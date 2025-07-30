from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import OuterRef, Subquery
from django.db.models.aggregates import Count, Max
from django.http import Http404, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.timezone import make_aware
from django.views.generic import ListView, TemplateView

from loguru import logger as log

from . import tasks
from .models import (
    DeliveryGroup,
    Machine,
    Session,
    SessionProperties,
    Task,
    Issue,
    Notification,
    PpmsBooking,
    Reservation,
)


class MachineList(ListView):
    queryset = {}
    template_name = "diop/machine_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        machines = Machine.objects.filter(active=True)
        for machine in machines:
            tr_class = ""
            if machine.powerstate == "off":
                tr_class = "table-danger"
            elif machine.maintenance:
                tr_class = "table-warning"
            elif machine.registration != "registered":
                tr_class = "table-info"
            machine.tr_class = tr_class

        context["machines"] = machines
        return context


class MachineListBasic(MachineList):
    queryset = {}
    template_name = "diop/machine_list_basic.html"


class SessionDetails(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        uid = kwargs.get("uid")
        context = {
            "session": Session.objects.get(uid=uid),
            "session_properties": SessionProperties.objects.filter(session=uid),
            "session_notifications": Notification.objects.filter(session=uid),
        }
        return render(request, "diop/session_details.html", context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)
        uid = kwargs.get("uid")

        if action is None:
            return HttpResponseBadRequest("Action missing.")
        elif action == "back":
            return redirect("session_list")

        if uid is None:
            return HttpResponseBadRequest("Session UID missing.")

        if action == "terminate":
            log.debug(f"Will request session [{uid}] to be terminated...")
            tasks.terminate_session(uid)
            return redirect("session_details", uid)

        elif action == "disconnect":
            log.debug(f"Will request session [{uid}] to be disconnected...")
            tasks.disconnect_session(uid)
            return redirect("session_details", uid)

        elif action == "message":
            # log.warning(request.POST)
            title = request.POST.get("msg-title", None)
            body = request.POST.get("msg-body", None)
            style = request.POST.get("btn-message-style", "Information")
            if not title or not body:
                return HttpResponseBadRequest("Message title or body missing.")

            log.debug(f"Will send a '{style}' message to session [{uid}]...")
            tasks.send_popup_message(uid, body, title, style)
            return redirect("session_details", uid)

        return HttpResponseBadRequest(f"Unknown action: [{action}]")


class SessionList(LoginRequiredMixin, ListView):
    def get_queryset(self):
        sort = self.request.GET.get("sort", "uid")
        last_props = SessionProperties.objects.filter(session=OuterRef("pk")).order_by(
            "-t_change"
        )
        cur_sessions = (
            Session.objects.filter(t_end=None)
            .annotate(state=Subquery(last_props.values("state")[:1]))
            .annotate(client_address=Subquery(last_props.values("client_address")[:1]))
            .annotate(t_change=Subquery(last_props.values("t_change")[:1]))
            .order_by(sort)
        )

        return cur_sessions


class ReservationDetails(LoginRequiredMixin, ListView):
    queryset = {}
    template_name = "diop/reservation_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get("id")  # NOTE: self.kwargs != kwargs
        context["res_id"] = id
        context["res"] = Reservation.objects.get(id=id)
        context["bookings"] = PpmsBooking.objects.filter(reservation=id).order_by(
            "t_start"
        )
        return context


class OperatorsDash(UserPassesTestMixin, TemplateView):

    template_name = "diop/operators_dash.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest = SessionProperties.objects.filter(session=OuterRef("pk")).order_by(
            "-t_change"
        )
        cur_sessions = Session.objects.filter(t_end=None).annotate(
            latest_state=Subquery(latest.values("state")[:1])
        )
        active = cur_sessions.filter(latest_state="active").count()
        disconnected = cur_sessions.exclude(latest_state="active").count()

        context["sessions_active_count"] = active
        context["sessions_disconnected_count"] = disconnected

        context["booking_groups"] = DeliveryGroup.objects.filter(booking_required=True)

        context["reservations_current"] = Reservation.objects.filter(
            t_start__lte=make_aware(datetime.now()),
            t_end__gte=make_aware(datetime.now()),
        ).order_by("user", "-t_end")

        context["reservations_future"] = Reservation.objects.filter(
            t_start__gte=make_aware(datetime.now()),
        ).order_by("user", "-t_end")

        return context

    def test_func(self):
        """Verify the user is a member of the 'Operators' or 'Admins' group.

        Used by the UserPassesTestMixin class.

        Returns
        -------
        bool
        """
        user_groups = self.request.user.groups.all()
        for group in user_groups:
            if group.name in ["Operators", "Admins"]:
                return True
        return False

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action", None)

        if action is None:
            return HttpResponseBadRequest("Action missing.")

        if action == "ppms-pull-users":
            tasks.pull_ppms_users()
            return redirect("operators_dash")
        elif action == "ppms-pull-bookings":
            date = datetime.strptime(request.POST.get("booking-date"), r"%Y-%m-%d")
            days = int(request.POST.get("booking-days"))
            log.warning(f"Requesting bookings for {date} (+ {days-1} days)...")
            tasks.pull_ppms_bookings(date, days)
            return redirect("operators_dash")

        return HttpResponseBadRequest(f"Unknown action: [{action}]")


@staff_member_required
def update_item(request, item):
    referer = request.META.get("HTTP_REFERER", "/")
    if item == "machines":
        okay, fail = tasks.update_machine_status()
    elif item == "sessions":
        okay, fail = tasks.update_session_status()
    else:
        raise Http404("What should we update?")

    return redirect(referer)


def dg_states(request):
    dg_states = DeliveryGroup.objects.values(
        "machine__deliverygroup", "machine__state"
    ).annotate(count=Count("dg_name"))

    # first regroup the results into a dict using the DG name as the key:
    regroup = {}
    for dg_state in dg_states:
        dg = dg_state["machine__deliverygroup"]
        state = dg_state["machine__state"]
        count = dg_state["count"]
        if dg in regroup:
            regroup[dg][state] = count
        else:
            regroup[dg] = {state: count}

    # now use the dict to create a list of dicts:
    state_by_dg = []
    for key, val in regroup.items():
        tmp = {
            "name": key,
            "available": val.get("available", 0),
            "inuse": val.get("inuse", 0),
            "disconnected": val.get("disconnected", 0),
        }
        # log.warning(tmp)
        state_by_dg.append(tmp)

    # log.warning(state_by_dg)
    context = {
        "dg_states": state_by_dg,
    }

    return render(request, "diop/dg_availability.html", context)


@staff_member_required
def status_issues_unresolved(request):
    unresolved = Issue.objects.filter(resolved=False).count()
    if unresolved == 0:
        return HttpResponse("")

    context = {"issues_unresolved_count": unresolved}

    return render(request, "diop/status/issues_unresolved.html", context)


@staff_member_required
def last_update_item(request, item):
    task = f"diop.tasks.update_{item[:-1]}_status"
    log.debug(f"taskname: {task}")

    task_obj = Task.objects.filter(name=task).first

    context = {"item_name": item, "item_label": item.title(), "item_task": task_obj}

    return render(request, "diop/status/update_item.html", context)
