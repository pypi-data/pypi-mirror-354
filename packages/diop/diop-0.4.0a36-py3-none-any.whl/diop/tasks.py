"""DIOP tasks."""

from datetime import datetime, timedelta, date

from django.db.models import Count
from django.db.models.query import QuerySet
from django.conf import settings
from django.utils.timezone import make_aware, now

from loguru import logger as log

from .adapters.activedirectory import ActiveDirectory
from .adapters.ppms import BookingSystem
from .adapters import psytricks
from .decorators import fire_and_dont_forget, status_update_task
from .exceptions import UpdateMachinesError, UpdateSessionsError
from .models import (
    Machine,
    Session,
    Notification,
    User,
    SiteLog,
    DeliveryGroup,
    Reservation,
)
from .site import in_dry_run_mode
from .utils import send_support_email


_BROKER = psytricks.ResTricksClient()


@status_update_task
def update_machine_status():
    """Fetch machine states from Citrix and update DB."""
    db_model = Machine
    desc = "machine"
    _prepare_update(db_model, desc)
    okay, fail = _update_status(
        desc=desc,
        new_state=_BROKER.get_machine_status(),
        process_cb=psytricks.process_machine_info,
        details="DNSName",
        err_obj=UpdateMachinesError,
    )
    # TODO: check if all machines have been updated, otherwise add an entry in
    # the issues table
    log.success(f"🔁🖥🖥🖥  DONE updating machines (ok: {okay}, fail: {fail})")
    return okay, fail


@status_update_task
def update_session_status():
    """Fetch session states from Citrix and update DB."""
    db_model = Session
    desc = "session"
    _prepare_update(db_model, desc)
    okay, fail = _update_status(
        desc=desc,
        new_state=_BROKER.get_sessions(),
        process_cb=psytricks.process_session_info,
        details="Uid",
        err_obj=UpdateSessionsError,
    )
    _process_ended_sessions()
    log.success(f"🔁🎬🎬🎬 DONE updating sessions (ok: {okay}, fail: {fail})")
    return okay, fail


def _prepare_update(db_model, desc):
    """Prepare all entries in a given DB model for updating.

    Shortcut function to set the `updated` field to `False` for all entries in
    a given model / table.

    Parameters
    ----------
    db_model : django.db.models.Model
        The model to use
    desc : str
        A description to use in related messages.
    """
    count = db_model.objects.all().update(updated=False)
    log.debug(f"🖥🎬🖥🎬  Prepared {count} {desc} objects for updating...")


def _update_status(desc, new_state, process_cb, details, err_obj):
    """Update DB with current infrastructure status.

    Parameters
    ----------
    desc : str
        The description of what is being updated.
    new_state : list(dict)
        The parsed JSON containing the information used to updated the DB.
    process_cb : function
        The callback function to use for processing each item in `new_state`.
    details : str
        The key to use for extracting detail information on the item to be
        updated.
    err_obj : Exception
        The exception to raise in case any of the items fails updating.

    Returns
    -------
    okay, fail: int, int
        A tuple denoting how many entries were successfully updated and how
        many failed.

    Raises
    ------
    err_obj
        Raised in case one or more entries failed updating, exception type is
        as specified in the call.
    """
    log.debug(f"🖥🎬🖥🎬 Got details on {len(new_state)} {desc}s.")
    okay = fail = 0
    fail_details = []

    for entry in new_state:
        try:
            process_cb(entry)
            okay += 1
        except Exception as err:
            fail_details.append(entry[details])
            log.error(f"🖥  Updating {desc} [{entry[details]}] FAILED: {err}")
            fail += 1

    if fail > 0:
        raise err_obj(
            f"🖥  Updating DB status failed for one or more {desc}s!",
            fail_details,
            okay,
            fail,
        )

    log.info(f"🖥🎬🖥🎬  Updated details on {okay} {desc}s.")
    return okay, 0


def _process_ended_sessions():
    """Set session entries end timestamp for orphaned sessions."""
    sessions = Session.objects.filter(t_end=None).filter(updated=False)
    if not sessions:
        log.debug("🛑🎬🎬🎬 Checked for ended sessions, all good.")
        return

    for session in sessions:
        session.t_end = make_aware(datetime.now())
        session.updated = True
        session.save()
        log.success(f"🛑🎬 Registered {session} as ended in the DB!")
    log.info(f"🛑🎬🎬🎬✅ Updated {len(sessions)} ended session entries!")


@fire_and_dont_forget
def terminate_session(uid):
    """Terminate the session with the given UID.

    Parameters
    ----------
    uid : int
        A Citrix session UID whose machine should be requested to restart.

    Returns
    -------
    dict
        The parsed JSON response of the request's response as delivered by the
        diop.adapters.psytricks.ResTricksClient.
    """
    # TODO: refuse action if session information in DB is outdated!
    return psytricks.terminate_session(psy_session_uid=uid)


def disconnect_all_sessions(dry_run=False):
    """Send a "disconnect" request to all session in state "active".

    Parameters
    ----------
    dry_run : bool, optional
        If True no disconnect request will be sent, only a warning message will
        be logged instead. By default False.
    """
    sessions = Session.objects.filter(t_end=None)
    log.debug(f"🧾🖥🎬 Got {len(sessions)} session(s) from the DB.")
    for session in sessions:
        if session.cur_properties.state == "active":
            if dry_run:
                log.warning(f"DRY-RUN: session {session} would be disconnected...")
                continue
            _BROKER.disconnect_session(session.machine.fqdn)
            record = SiteLog(
                name="Session disconnected",
                session=session,
                user=session.user,
                machine=session.machine,
                deliverygroup=session.machine.deliverygroup,
                parameters=f"{session.user}@{session.machine.hostname}",
            )
            record.save()
        else:
            log.warning(f"Nothing to do for session {session}")


@fire_and_dont_forget
def disconnect_sessions_of(user):
    """Disconnect all sessions of the given username.

    Parameters
    ----------
    user : str
        The username for which sessions should be disconnected.
    """
    sessions = Session.objects.filter(t_end=None, user=user)
    log.debug(f"🧾🖥🎬 Got {len(sessions)} session(s) of [{user}] from the DB.")
    for session in sessions:
        _BROKER.disconnect_session(session.machine.fqdn)
        record = SiteLog(
            name="Session disconnected",
            session=session,
            user=session.user,
            machine=session.machine,
            deliverygroup=session.machine.deliverygroup,
            parameters=f"{session.user}@{session.machine.hostname}",
        )
        record.save()


@fire_and_dont_forget
def disconnect_session(uid):
    """Send a "disconnect" request to the session with the given UID.

    Parameters
    ----------
    uid : int
        The session UID that should be disconnected.
    """
    session = Session.objects.get(uid=uid)
    log.debug(f"🖥🎬📢 <disconnect> ⏩ [{uid}]@[{session.machine.fqdn}]")
    _BROKER.disconnect_session(session.machine.fqdn)
    record = SiteLog(
        name="Session disconnected",
        session=session,
        user=session.user,
        machine=session.machine,
        deliverygroup=session.machine.deliverygroup,
        parameters=f"{session.user}@{session.machine.hostname}",
    )
    record.save()


@fire_and_dont_forget
def send_popup_message(uid, message, title, style):
    """Send a pop-up message to the session with the given UID.

    Parameters
    ----------
    uid : int
        The UID of the session that should receive and show the pop-up message.
    message : str
        The message to show.
    title : str
        The title of the message
    style : str
        The message style. Refer to the [pyppms][pyppms] docs for details.
    """
    session = Session.objects.get(uid=uid)
    machine = session.machine.fqdn
    user = session.user
    notification = Notification(
        user=user,
        session=session,
        method="P",
        cc_adm=False,
        subject=title,
        body=message,
        creator="Interactive (web)",
    )
    notification.save()
    log.debug(f"🖥🎬📢 <send_message> ⏩ [{uid}]@[{machine}]")
    _BROKER.send_message(machine, message, title, style)
    notification.t_sent = make_aware(datetime.now())
    notification.save()


@status_update_task
def pull_ppms_users(force_refresh=False):
    """Update DIOP users table with PPMS details."""
    log.success("Requesting update of PPMS users...")
    ppms = BookingSystem()
    return ppms.pull_users(force_refresh)


@status_update_task
def pull_ppms_bookings(dt=None, days=1):
    """Update DIOP reservations from PPMS bookings.

    Parameters
    ----------
    dt : date, optional
        The date to pull PPMS bookings for, by default None which will result in
        today's bookings being fetched.
    days : int, optional
        The number of follow-up days to pull from PPMS (plus one), by default 1
        which will result in only the date given as `dt` being fetched.

    Returns
    -------
    int, int
        A tuple with counts of success / failed booking updates.
    """
    # don't put `date.today()` as the default parameter value, this will become
    # static when being run through django-q2:
    if not dt:
        dt = date.today()
    okay = fail = 0
    ppms = BookingSystem()
    for delta in range(days):
        pull_date = dt + timedelta(days=delta)
        d_okay, d_fail = ppms.pull_bookings(dt=pull_date)
        okay += d_okay
        fail += d_fail

    return okay, fail


def process_maintenance_requests():
    """Check the 'req_maintenance' Machine flag and set maintenance accordingly.

    This function is intended to be run regularly by a scheduled tasks, it will
    check the "maintenance requested" flag for each machine and will assemble
    a list of machines that should be placed in maintenance mode (skipping
    those machines that are having an active session as users won't be able to
    reconnect to them once a machine is in maintenance) and a list of machines
    that should have maintenance disabled.

    Eventually `set_maintenance()` is called with those two lists to actually
    request the maintenance state adjustments.
    """
    # enabling maintenance this way is only done if there is no session on it:
    enable_on = []
    want_maintenance = Machine.objects.filter(req_maintenance=True)
    for machine in want_maintenance:
        try:
            session = Session.objects.get(machine=machine, t_end=None)
            log.debug(
                f"Machine {machine} is having a session ({session}), not placing "
                "in maintenance mode!"
            )
        except Session.DoesNotExist:
            enable_on.append(machine)

    # disabling maintenance can be done independently of a session:
    disable_on = Machine.objects.filter(req_maintenance=False)

    psytricks.set_maintenance(disable_on=disable_on, enable_on=enable_on)


def check_session_constraints(max_parallel=1):
    """Call all session constraint checking functions.

    Parameters
    ----------
    max_parallel : int, optional
        The maximum number of parallel sessions allowed, by default 1.
    """
    check_session_max_parallel(max_parallel)


def check_session_disconnect_time():  # WIP
    """Check disconnected sessions exceeding the (per-user) time limit.

    Using `diop.models.session.Session.exceeds_disconnected_limit`
    """
    sessions = Session.objects.filter(t_end=None)
    for session in sessions:
        if session.exceeds_disconnected_limit:
            log.warning(f"Session [{session}] is above the disconnection limit!")
            send_support_email("ops-disconnect-limit", {"session": session})


def check_session_max_parallel(limit=1):
    """Check sessions for violations of the max-parallel-sessions constraint.

    Query the DB for running sessions (i.e. that do not have an end time) that
    belong to any of the delivery groups having the `unique_session` attribute
    set and count the number of sessions for each user.

    If a user is having more sessions than allowed, assemble some details and
    send a pop-up notification to *each* of those sessions.

    By running this with the frequent housekeeping tasks it is ensured that a
    user gets almost instant feedback on the multiple sessions after starting
    a new one.

    Parameters
    ----------
    limit : int, optional
        The maximum count of parallel sessions in the DG's having the
        `unique_session` attribute set allowed for each user, by default 1.
    """
    unique_sess_dgs = DeliveryGroup.objects.filter(unique_session=True)
    violating = (
        Session.objects.filter(t_end=None, machine__deliverygroup__in=unique_sess_dgs)
        .values("user")
        .annotate(session_count=Count("user"))
        .filter(session_count__gt=limit)
    )
    if not violating:
        log.debug("No session violating the max-parallel-sessions constraint.")
        return

    dg_names = ", ".join(unique_sess_dgs.values_list("dg_name", flat=True))

    for multi in violating:
        username = multi["user"]
        count = multi["session_count"]
        sessions = Session.objects.filter(user=username, t_end=None).order_by("uid")
        uid_machine = "- " + "\n- ".join([f"({x.uid}) {x.machine}" for x in sessions])
        log.debug(f"User [{username}] is having {count} parallel sessions!")
        context = {
            "user": User.objects.get(pk=username),
            "uid_machine": uid_machine,
            "unique_sesssion_group_names": dg_names,
        }
        for session in sessions:
            Notification.new_popup(
                psytricks.send_popup, session.uid, "multi-sessions", context
            )


def check_reservations():
    """Check reservations for all DG's requiring booking.

    For each Delivery Group that requires booking the corresponding reservations
    will be checked and the status of user access permissions will be updated in
    the Diop DB.

    See Also
    --------
    check_reservations_for_dg
    """
    booking_groups = DeliveryGroup.objects.filter(booking_required=True)
    for dg in booking_groups:
        check_reservations_for_dg(dg)
        psytricks.update_diop_dg_access(dg_name=dg.dg_name)


def check_reservations_for_dg(dg: DeliveryGroup):  # WIP
    """Check reservations, enable DG access, send warnings, terminate sessions.

    Check all reservations and perform the following tasks:

    -  Ensure each user with a valid reservation is having access to the
       delivery group (DG) of the same name.
    - If a reservation is about to expire (< 10 minutes), send a notification
      (pop-up and email) to the user.
    - If a user doesn't have a valid reservation any more:
      - terminate their session in the DG (warn only in dry-run mode)
      - remove access to the DG
    - Send a notification to users having a running reservation >5m but no
      session. This will also serve as a reminder to cancel remaining booked
      time after finishing a session.
    - Re-send the reminder after 30m, Cc admins.

    Parameters
    ----------
    dg : DeliveryGroup
        The DG to process.
    """
    log.debug(f"Checking reservations for group [{dg.dg_name}]...")
    users_with_res = Reservation.running_usernames(dg.dg_name)

    log.debug(f"Adjusting access permissions for DG [{dg.dg_name}]...")
    psytricks.set_dg_access(
        dg_name=dg.dg_name,
        usernames=users_with_res,
        keep_common=settings.DIOP_GRACEFUL,
    )

    check_stale_reservations(dg=dg, users=users_with_res)

    # get active sessions of the current DG:
    sessions = Session.objects.filter(machine__deliverygroup=dg, t_end=None)
    for session in sessions:
        check_reservation_ending_soon(session)

        if not session.user.accessgroup_member:
            log.info(
                f"User [{session.user.username}] is not a member of the accessgroup, "
                "not checking session for a valid reservation (might be an admin)."
            )
            continue

        if session.user.username in users_with_res:
            continue

        if in_dry_run_mode("terminating session without reservation"):
            sent = Notification.new_email(
                user=session.user,
                template="session-without-reservation",
                context={
                    "dg_name": dg.dg_name,
                    "session": session,
                },
                support="",
                session=session,
            )
            if sent:
                log.warning(
                    "Sent notification email on session without valid reservation: "
                    f"{session} [{dg}]"
                )
            continue

        log.warning(f"Terminating session {session}, no valid reservation!")
        psytricks.terminate_session(d_session=session)
        record = SiteLog(
            name="Session terminated (reservation expired)",
            session=session,
            user=session.user,
            machine=session.machine,
            deliverygroup=session.machine.deliverygroup,
        )
        record.save()
        sent = Notification.new_email(
            user=session.user,
            template="session-terminated",
            context={
                "dg_name": dg.dg_name,
                "session": session,
            },
            support="",
            session=session,
        )
        if sent:
            log.warning(
                "Sent notification email on terminated 🎫🛑🎬 session: "
                f"{session} [{dg}]"
            )


def check_stale_reservations(dg: DeliveryGroup, users: QuerySet):
    """Check for reservations that do not have a session.

    Identify reservations of the given users in the specified DG that do not
    have an active session in that DG and process them.

    Parameters
    ----------
    dg : DeliveryGroup
        _description_
    users : django.db.models.query.QuerySet
        A queryset containing users having a currently running reservation.
    """
    users_with_session = Session.objects.filter(
        machine__deliverygroup=dg, t_end=None
    ).values_list("user__username", flat=True)

    res_but_no_session = users.difference(users_with_session)
    log.debug(f"Reservations without corresponding session: {len(res_but_no_session)}")
    stale = Reservation.running(dg).filter(user__username__in=res_but_no_session)
    for reservation in stale:
        process_stale_reservation(reservation)


def process_stale_reservation(
    reservation: Reservation, soft: int = 5, hard: int = 30, remaining: int = 15
):
    """Process 'stale' reservations, i.e. NOT having a corresponding session.

    If the reservation start is more than the given "soft" limit minutes ago,
    send an email notification to the user, if it's more than the "hard" limit
    minutes ago, re-send the notification with Cc'ing admins.

    Parameters
    ----------
    reservation : Reservation
        The reservation object to check.
    soft : int, optional
        The "soft" limit in minutes, after which a notification is sent to the
        user, by default 5.
    hard : int, optional
        The "hard" limit in minutes, after which the notification will be
        re-sent to the user AND the admins, by default 30.
    remaining : int, optional
        The "remaining" limit in minutes: if a stale reservation has less than
        the given number of minutes (default=15) left, nothing will be done.
        This is intended to prevent sending pointless notifications to users for
        reservations that are about to expire anyway.

    Returns
    -------
    bool
        True in case a notification was sent, False otherwise.
    """
    # calculate limit values in seconds:
    lim_hard = hard * 60
    lim_soft = soft * 60
    lim_remaining = remaining * 60

    if reservation.till_end < lim_remaining:
        log.debug(
            f"Reservation {reservation} has less than {remaining}m left, ignoring."
        )
        return False

    since_start = reservation.since_start
    if since_start < lim_soft:
        log.debug(
            f"Reservation {reservation} only started {since_start}s ago, ignoring."
        )
        return False

    dg = reservation.deliverygroup
    user = reservation.user

    # default notification properties (will be overridden below if necessary):
    template = "stale-reservation"
    support = ""  # do not Cc admins
    context = {
        "reservation": reservation,
        "dg_name": dg.dg_name,
        "delta": soft,
    }

    # reservation start delta is above the hard limit, Cc admins:
    if since_start > lim_hard:
        context["delta"] = hard
        support = "cc"

    # check if there has been an actual session during the lifetime of this
    # reservation and send a reminder to cancel the leftover time:
    last_completed = Session.last_completed(dg=dg, user=user)
    log.trace(f"last_completed.t_end: {last_completed.t_end}")
    log.trace(f"reservation.t_start: {reservation.t_start}")
    if last_completed.t_end > reservation.t_start:
        support = ""  # do not Cc admins
        context["delta"] = remaining
        template = "remaining-reservation-time-please-cancel"
        context["last_completed"] = last_completed
        ended = (now() - last_completed.t_end).total_seconds()
        log.trace(f"Session related to res {reservation} ended {ended}s ago.")
        if ended > lim_hard:
            log.trace(f"Session end more than {hard}m ago, will Cc admins...")
            support = "cc"

    sent = Notification.new_email(
        user=reservation.user,
        template=template,
        context=context,
        support=support,
    )
    return sent


def check_reservation_ending_soon(session: Session, threshold: int = 10):
    """Check if a session's reservation is about to expire and send a warning.

    The given session will be checked for its corresponding reservation. In case
    the remaining runtime of the reservation is below the threshold a warning
    will be sent to the session owner (via pop-up and email).

    Parameters
    ----------
    session : Session
        The session to check the reservation for.
    threshold : int
        The remaining reservation time threshold in minutes, default=10.

    Returns
    -------
    bool
        True in case the remaining reservation time is below the given
        threshold, False otherwise.
    """
    dg = session.machine.deliverygroup
    reservation = Reservation.ending_in_less_than(
        minutes=threshold, dg_name=dg.dg_name, username=session.user.username
    ).first()  # only the first is required here (even if there were multiple)

    if not reservation:
        return False

    context = {
        "reservation": reservation,
        "session": session,
        "dg_name": reservation.deliverygroup.dg_name,
    }
    Notification.new_popup(
        psytricks.send_popup, session.uid, "reservation-ending-soon", context
    )
    Notification.new_email(session.user, "reservation-ending-soon", context)

    return True


@fire_and_dont_forget
def send_session_reminders():
    """Send a reminder email for each disconnected session."""
    sessions = Session.objects.filter(t_end=None)
    for session in sessions:
        if session.cur_state != "disconnected":
            continue

        log.debug(f"Sending session reminder for {session}...")
        context = {
            "session": session,
        }
        Notification.new_email(
            user=session.user,
            template="session-reminder",
            context=context,
            session=session,
        )


@status_update_task
def update_users_from_ad():
    """Update all users from AD that are members of the access-group.

    In step one, it is made sure for each user exists a corresponding Diop user
    record and the values of the attributes `fullname`, `department` and `email`
    is set according to the information from AD. In addition, their
    `accessgroup_member` attribute is set to `True`.

    In the second step the Diop DB is queried for entries whose usernames are
    NOT in the list of users of the AD access-group to make sure their
    `accessgroup_member` attribute is set to `False`.
    """
    ad_conn = ActiveDirectory()
    # fetch users from AD, this will also fill the `ad_conn.user_details` dict:
    ad_group_members = ad_conn.group_members_usernames

    # part 1: ensure user record exists and has consistent data:
    for ad_username in ad_group_members:
        ad_user = ad_conn.user_details[ad_username]
        User.is_up_to_date_from_ad(user_details=ad_user, accessgroup_member=True)

    # part 2: ensure all other accounts have 'accessgroup_member' set to False:
    non_members = User.objects.exclude(username__in=ad_group_members)
    for non_member in non_members:
        if non_member.accessgroup_member:
            log.debug(f"Accessgroup membership [{non_member.username}] -> False")
            non_member.accessgroup_member = False
            non_member.save()


@status_update_task
def housekeeping_every_minute():
    """Regular housekeeping tasks that should be done every minute.

    Run various checks on the status of the DIOP DB:
    - [ ] age of sessions and machines status
    - [ ] age of last PPMS sync
    - [ ] age of last LDAP sync
    - [ ] terminate long-disconnected sessions
    - [x] put a machine in maintenance mode if requested and no session
    - [x] double sessions logic (warn, then terminate after 1h?)
    - [x] enable / disable access to DG's depending on reservation status
    - [x] terminate sessions whose reservation expired
    - [ ] users whose AD account was disabled
    - ...
    """
    process_maintenance_requests()
    check_session_constraints()
    check_reservations()


@status_update_task
def housekeeping_start_of_day():
    """Housekeeping tasks to be run at the start of a day, e.g. at 09:00.

    - [ ] platform summary: sessions, storage, deltas, users, ...
    - [x] disconnection time reminder (-> once a day, not once a minute!)
    - [ ] users without a PPMS account (required for billing)
    """
    send_session_reminders()


@fire_and_dont_forget
def housekeeping_early_morning():
    """Housekeeping tasks to be run at the very early morning, e.g. at 04:00.

    The idea of these tasks is to run them at a time with the lowest probability
    of any user actively working.

    - [x] disconnect all active sessions
    """
    dry_run = in_dry_run_mode("disconnecting active sessions")
    disconnect_all_sessions(dry_run=dry_run)
