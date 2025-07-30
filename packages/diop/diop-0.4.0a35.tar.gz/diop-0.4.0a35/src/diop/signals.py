from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from loguru import logger as log

from .models import (
    SiteLog,
    User,
    Reservation,
    Notification,
    Session,
    SessionProperties,
    Machine,
)


@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    log.trace(f"Received user post-save signal (created={created}): {instance}")

    if created:
        name = "User added"
    else:
        name = "User modified"

    record = SiteLog(name=name, user=instance, details=instance.full_details)
    record.save()

    # update the disconnected_max value with the default in case it's 0:
    User.objects.filter(pk=instance.pk, disconnected_max=0).update(
        disconnected_max=settings.DIOP_DISCONNECTED_MAX
    )


# FIXME: add a signal handler for deleting reservations!!


@receiver(post_save, sender=Reservation)
def reservation_post_save_handler(sender, instance, created, **kwargs):
    log.trace(f"Received reservation post-save signal (created={created}): {instance}")

    if created:
        name = "Reservation added"
    else:
        name = "Reservation modified"

    record = SiteLog(
        name=name,
        reservation=instance,
        user=instance.user,
        deliverygroup=instance.deliverygroup,
        details=str(instance),
    )
    record.save()


@receiver(post_save, sender=Notification)
def notification_post_save_handler(sender, instance, created, **kwargs):
    notification = instance
    if not notification.t_sent:
        log.debug(f"Notification created but not sent yet: {notification}")
        return

    log.trace(f"Notification post-save signal (created={created}): {notification}")

    details = (
        f"{notification}\n\n"
        f"method=[{notification.method}]\n"
        f"cc_adm=[{notification.cc_adm}]\n"
        f"t_created=[{notification.t_created}]\n"
        f"t_sent=[{notification.t_sent}]\n"
        f"creator=[{notification.creator}]\n"
        f"subject=[{notification.subject}]\n"
        f"body=[{notification.body}]\n"
    )

    # email notifications don't necessarily have a session (and therefore machine, ...)
    machine = deliverygroup = None
    if notification.session:
        machine = notification.session.machine
        deliverygroup = notification.session.machine.deliverygroup

    record = SiteLog(
        name="Notification sent",
        parameters=f"subject=[{notification.subject}]",
        notification=notification,
        session=notification.session,
        user=notification.user,
        machine=machine,
        deliverygroup=deliverygroup,
        details=details,
    )
    record.save()


@receiver(post_save, sender=Machine)
def machine_post_save_handler(sender, instance, created, **kwargs):
    machine = instance
    log.trace(f"Machine post-save signal (created={created}): {machine}")

    details = (
        f"{machine}\n"
        f"state=[{machine.state}]\n"
        f"powerstate=[{machine.powerstate}]\n"
        f"maintenance=[{machine.maintenance}]\n"
        f"registration=[{machine.registration}]\n"
        f"agent=[{machine.agent}]\n"
        f"active=[{machine.active}]\n"
        f"req_maintenance=[{machine.req_maintenance}]\n"
    )

    maint_short = "maint" if machine.maintenance else "no-maint"
    reg_short = "reg" if machine.registration == "registered" else "unreg"
    parameters = f"{machine.powerstate} | {machine.state} | {reg_short} | {maint_short}"

    log_name = "Machine status changed"
    if created:
        log_name = "Machine added"

    record = SiteLog(
        name=log_name,
        machine=machine,
        deliverygroup=machine.deliverygroup,
        parameters=parameters,
        details=details,
    )
    record.save()


@receiver(post_save, sender=Session)
def session_post_save_handler(sender, instance, created, **kwargs):
    session = instance
    log.trace(f"Session post-save signal (created={created}): {session}")

    details = (
        f"{session}\n"
        f"machine=[{session.machine}]\n"
        f"user=[{session.user}]\n"
        f"t_start=[{session.t_start}]\n"
        f"t_end=[{session.t_end}]\n"
    )

    log_name = "Session ended"
    if created:
        log_name = "Session started"

    record = SiteLog(
        name=log_name,
        session=session,
        user=session.user,
        machine=session.machine,
        deliverygroup=session.machine.deliverygroup,
        parameters=f"t_start=[{session.t_start}]",
        details=details,
    )
    record.save()


@receiver(post_save, sender=SessionProperties)
def sessionproperties_post_save_handler(sender, instance, created, **kwargs):
    props = instance
    log.trace(f"SessionProperties post-save signal (created={created}): {props}")

    details = (
        f"{props}\n"
        f"state=[{props.state}]\n"
        f"t_change=[{props.t_change}]\n"
        f"client_address=[{props.client_address}]\n"
        f"client_name=[{props.client_name}]\n"
        f"client_version=[{props.client_version}]\n"
    )

    record = SiteLog(
        name="Session Properties changed",
        parameters=f"state=[{props.state}]",
        session=props.session,
        user=props.session.user,
        machine=props.session.machine,
        deliverygroup=props.session.machine.deliverygroup,
        details=details,
    )
    record.save()
