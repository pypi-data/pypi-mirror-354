"""Diop util methods."""

from smtplib import SMTPException
from sys import stderr

from django.conf import settings
from django.core.mail import EmailMessage
from django.utils.timezone import make_naive

from loguru import logger as log

from . import site
from .models.message_template import MessageTemplate


def naive_minutes(dt_obj):
    """Format a `datetime` to minute precision after running `make_naive` on it.

    Parameters
    ----------
    dt_obj : datetime.datetime
        The datetime object to format.
    """
    return make_naive(dt_obj).strftime(r"%Y-%m-%d %H:%M")


def send_email(
    subject: str, body: str, to: str, support: str = "", prefix: bool = True
):
    """Send an email.

    Simplifies things like deriving the sender address, putting a site-label
    prefix into the subject and dealing with cc/bcc-ing administrators.

    Parameters
    ----------
    subject : str
        The email subject.
    body : str
        The email body / content.
    to : str
        A single recipient address.
    support : str, optional
        If set to `cc` or `bcc` the address set in `DIOP_SUPPORT_CONTACT`
        will be added as a respective recipient. By default empty.
    prefix : bool, optional
        If set to `True` a site-specific label will be prefixed to the subject,
        enclosed in square brackets, otherwise the subject will not be touched
        (by default True).

    Raises
    ------
    SMTPException
        Raised in case sending the email failed.
    """

    cc = bcc = []
    if support == "cc":
        cc = [settings.DIOP_SUPPORT_CONTACT]
    elif support == "bcc":
        bcc = [settings.DIOP_SUPPORT_CONTACT]

    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=f"{site.name()} Support <{settings.DIOP_SUPPORT_CONTACT}>",
        to=[to],
        cc=cc,
        bcc=bcc,
    )
    try:
        email.send(fail_silently=False)
    except SMTPException as err:
        log.error(f"Sending email to [{to}] failed: {err.with_traceback}")
        raise err


def send_support_email(template: str, context: dict):
    """Shorthand to send a mail to the `DIOP_SUPPORT_CONTACT` address.

    Parameters
    ----------
    template : str
        The name of the template to use for the message.
    context : dict
        The context dict required to render the template.
    """
    support = settings.DIOP_SUPPORT_CONTACT
    msg = MessageTemplate.render_message(template, context)
    send_email(msg.subject, msg.body, to=support)


def set_loglevel(level: str = "TRACE"):
    """Shorthand to adjust the logging level going to stderr.

    Mostly (but not exclusively) useful when interactively testing functionality
    using the `shell_plus` extension.

    Parameters
    ----------
    level : str, optional
        The level name, by default "TRACE".
    """
    log.remove()
    log.add(stderr, level=level)
