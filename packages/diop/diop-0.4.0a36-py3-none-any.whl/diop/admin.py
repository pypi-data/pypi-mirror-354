from django.contrib import admin

from loguru import logger as log

from .models import (
    User,
    Machine,
    DeliveryGroup,
    Session,
    SessionProperties,
    Task,
    Issue,
    Notification,
    Reservation,
    PpmsBooking,
    SiteLog,
    MessageTemplate,
)

# globally disable "delete selected" action:
admin.site.disable_action("delete_selected")


class SessionInline(admin.TabularInline):
    model = Session
    readonly_fields = ("uid", "machine", "user", "t_start")
    exclude = ["t_end"]
    show_change_link = True
    can_delete = False
    extra = 0


class SessionPropertiesInline(admin.TabularInline):
    model = SessionProperties
    readonly_fields = (
        "t_change",
        "state",
        "client_address",
        "client_version",
    )
    exclude = ["client_name"]
    show_change_link = True
    can_delete = False
    extra = 0


@admin.register(DeliveryGroup)
class DeliveryGroupAdmin(admin.ModelAdmin):
    list_display = ("dg_name", "booking_required", "unique_session", "host_prefix")


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = (
        "hostname",
        "deliverygroup",
        "maintenance",
        "state",
        "powerstate",
        "active",
        "updated",
        "req_maintenance",
    )
    actions = [
        "request_maintenance",
    ]
    list_filter = [
        "deliverygroup",
        "maintenance",
        "state",
        "active",
        "updated",
        "req_maintenance",
    ]
    readonly_fields = [
        "fqdn",
        "hostname",
        "deliverygroup",
        "registration",
        "maintenance",
        "agent",
        "state",
        "powerstate",
        "updated",
    ]
    search_fields = ("fqdn",)

    @admin.action(description="Toggle 'Request Maintenance'")
    def request_maintenance(self, request, queryset):
        for machine in queryset:
            log.info(f"Toggling 'Request maintenance' for [{machine}]")
            machine.req_maintenance = not (machine.req_maintenance)
            machine.save()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "fullname",
        "ppms_fullname",
        "email",
        "groupname",
        "ppms_group",
        "department",
        "gracetime",
        "disconnected_max",
        "enabled",
        "accessgroup_member",
    )
    list_filter = [
        "enabled",
        "accessgroup_member",
        "gracetime",
        "disconnected_max",
        "department",
        "groupname",
        "ppms_group",
    ]
    search_fields = (
        "username",
        "fullname",
        "ppms_fullname",
        "email",
        "groupname",
        "ppms_group",
        "department",
    )
    readonly_fields = [
        "username",
        "email",
        "fullname",
        # "ppms_fullname",  # FIXME: should this be read-only...?
        # "ppms_group",  # FIXME: should this be read-only...?
        "accessgroup_member",
        "enabled",
    ]
    # TODO: reactivate inlines once the django-edit-bug is fixed
    # inlines = [SessionInline]


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("uid", "machine", "user", "t_start", "t_end")
    list_filter = ["t_end", "user", "machine"]
    readonly_fields = [
        "uid",
        "machine",
        "user",
        "t_start",
        "t_end",
        "updated",
    ]
    # TODO: reactivate inlines once the django-edit-bug is fixed
    # inlines = [SessionPropertiesInline]


@admin.register(SessionProperties)
class SessionPropertiesAdmin(admin.ModelAdmin):
    list_display = ("session", "t_change", "state", "client_address")
    list_filter = ["session", "state"]
    readonly_fields = [
        "session",
        "t_change",
        "state",
        "client_address",
        "client_name",
        "client_version",
    ]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "t_start",
        "t_end",
        "unfinished",
        "failed",
        "description",
    )
    list_filter = ["name", "failed"]


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = (
        "severity",
        "timestamp",
        "resolved",
        "task",
        "user",
        "description",
    )
    list_filter = ["resolved", "severity", "task", "user"]
    actions = [
        "mark_resolved",
    ]
    search_fields = ("description",)

    @admin.action(description="Mark as resolved")
    def mark_resolved(self, request, queryset):
        for issue in queryset:
            log.info(f"Marking issue as resolved: {issue}")
            issue.resolved = True
            issue.save()


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "session",
        "method",
        "cc_adm",
        "subject",
        "t_created",
        "t_sent",
        "creator",
    )
    list_filter = [
        "t_sent",
        "method",
        "cc_adm",
        "user",
    ]
    search_fields = (
        "subject",
        "body",
    )
    readonly_fields = [
        "user",
        "session",
        "method",
        "cc_adm",
        "subject",
        "body",
        "t_created",
        "t_sent",
        "creator",
    ]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "deliverygroup",
        "t_start",
        "t_end",
    )
    list_filter = [
        "t_start",
        "deliverygroup",
        "user",
    ]
    readonly_fields = [
        "user",
        "deliverygroup",
        "t_start",
        "t_end",
    ]


@admin.register(PpmsBooking)
class PpmsBookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "system_id",
        "t_start",
        "t_end",
        "ppms_session",
        "sync_state",
        "reservation",
    )
    list_filter = [
        "t_start",
        "sync_state",
        "username",
    ]
    readonly_fields = [
        "username",
        "system_id",
        "t_start",
        "t_end",
        "ppms_session",
        "sync_state",
        "reservation",
    ]


@admin.register(SiteLog)
class SiteLogAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "parameters",
        "time",
        "user",
        "deliverygroup",
        "machine",
        "session",
        "task",
        "notification",
        "reservation",
    )
    list_filter = [
        "name",
        "time",
        "deliverygroup",
        "machine",
        "user",
    ]
    readonly_fields = [
        "name",
        "parameters",
        "time",
        "details",
        "user",
        "deliverygroup",
        "machine",
        "session",
        "task",
        "notification",
        "reservation",
    ]


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "subject")
