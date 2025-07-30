"""Diop Notification model."""

from typing import Callable

from django.db import models
from django.utils.timezone import now

from loguru import logger as log

from ..utils import send_email
from .user import User
from .session import Session
from .message_template import MessageTemplate


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        POP_UP = "P"
        EMAIL = "E"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="User which the notification is addressed to.",
        null=False,
        blank=False,
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        help_text="Session the notification relates to.",
        null=True,
        blank=True,
    )
    method = models.CharField(
        max_length=1,
        choices=NotificationType.choices,
        default=NotificationType.POP_UP,
        verbose_name="Delivery Method",
        help_text="How the notification should be delievered to the user.",
    )
    cc_adm = models.BooleanField(
        verbose_name="Cc Operators",
        help_text="Flag if admins should be notified as well.",
    )
    subject = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        verbose_name="The notification subject / title.",
    )
    body = models.TextField(
        null=False,
        blank=False,
        verbose_name="The notification body / content.",
    )
    t_created = models.DateTimeField(
        verbose_name="Creation Time",
        help_text="Notification creation timestamp.",
        null=False,
        default=now,
    )
    t_sent = models.DateTimeField(
        verbose_name="Sent Time",
        help_text="Notification delivery timestamp (empty if not yet delieverd).",
        null=True,
    )
    creator = models.CharField(
        verbose_name="Creator",
        max_length=64,
        help_text="Creator / origin of the notification.",
        blank=True,
    )

    def __str__(self):
        return f"{self.user.email} [{self.subject}]"

    @classmethod
    def new_popup(cls, send_popup: Callable, uid: int, template: str, context: dict):
        """Send a pop-up notification unless it has already been sent before.

        Parameters
        ----------
        send_popup : Callable
            A callable taking care of delivering the message to a session.
        uid : int
            The session UID.
        template : str
            The name of the template to use for the message.
        context : dict
            The context dict required to render the template.
        """
        try:
            msg = MessageTemplate.render_message(template, context)
        except Exception as ex:
            log.error(f"Rendering message template [{template}] failed: {ex}")
            return False

        session = Session.objects.get(pk=uid)
        if (
            cls.objects.exclude(t_sent=None)
            .filter(
                user=session.user,
                session=session,
                method=cls.NotificationType.POP_UP,
                subject=msg.subject_raw,
                body=msg.body_raw,
            )
            .exists()
        ):
            log.trace("Message has been delivered before, not re-sending.")
            return False

        notification = cls(
            user=session.user,
            session=session,
            method="P",
            cc_adm=False,
            subject=msg.subject_raw,
            body=msg.body_raw,
        )
        notification.save()
        machine = session.machine.fqdn
        log.debug(f"🖥🎬📢 <send_message> ⏩ [{uid}]@[{machine}]")
        sent = send_popup(
            machine=machine,
            body=msg.body,
            subject=msg.subject,
            category=msg.category,
        )
        if sent:
            notification.t_sent = now()
            notification.save()
            return True

        # should we raise an exception instead, to distinguish between messages
        # that have been sent before (no-re-delivery) and sending errors?
        return False

    @classmethod
    def new_email(
        cls,
        user: User,
        template: str,
        context: dict,
        support: str = "",
        session: Session = None,
    ):
        """Send an email notification unless it has already been sent before.

        If a message is actually sent, a new notification will be recorded in
        the DB, containing all relevant properties of the message. To ensure
        this record is independent of external circumstances, the "raw" versions
        of the message subject and body will be used, i.e. the strings that were
        rendered from the given template with all Django template filters being
        stripped. This ensures messages will not be re-sent if e.g. a
        `naturaltime` filter produces a different result to when the
        notification has been initially recorded in the DB.

        Attempting to send an identical message multiple times with different
        values for the `support` parameter (e.g. once with `support=""` and
        once with `support="cc"` or `support="bcc"`) will deliver the message
        twice, once only to the user and once having the admins in Cc.

        Parameters
        ----------
        user : User
            The Diop user related to this email.
        template : str
            The name of the template to use for the message.
        context : dict
            The context dict required to render the template.
        support : str, optional
            If set to `cc` or `bcc` the address set in `DIOP_SUPPORT_CONTACT`
            will be added as a respective recipient. By default empty.
        session : Session, optional
            An optional session object that is related to this email (will be
            used to link the created notification in the DB accordingly). By
            default `None`.

        Raises
        ------
        SMTPException
            May be raised by the `send_email()` call.

        Returns
        -------
        bool
            True in case the email was sent, False (e.g. rendering failed, or
            the message has already been sent before) otherwise.
        """
        try:
            msg = MessageTemplate.render_message(template, context)
        except Exception as ex:
            log.error(f"Rendering message template [{template}] failed: {ex}")
            return False

        if (
            cls.objects.exclude(t_sent=None)
            .filter(
                user=user,
                session=session,
                method=cls.NotificationType.EMAIL,
                cc_adm=True if support in ["cc", "bcc"] else False,
                subject=msg.subject_raw,
                body=msg.body_raw,
            )
            .exists()
        ):
            log.trace("Message has been delivered before, not re-sending.")
            return False

        notification = cls(
            user=user,
            session=session,
            method=cls.NotificationType.EMAIL,
            cc_adm=True if support in ["cc", "bcc"] else False,
            subject=msg.subject_raw,
            body=msg.body_raw,
        )
        notification.save()

        send_email(subject=msg.subject, body=msg.body, to=user.email, support=support)

        notification.t_sent = now()
        notification.save()
        return True
