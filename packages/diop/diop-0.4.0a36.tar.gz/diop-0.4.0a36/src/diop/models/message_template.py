"""Diop MessageTemplate model."""

import re

from box import Box

from django.conf import settings
from django.db import models
from django.template import Template, Context

from .. import site


class MessageTemplate(models.Model):
    class Meta:
        verbose_name = "Message Template"

    class MessageCategory(models.TextChoices):
        QUESTION = "Q"
        INFO = "I"
        WARNING = "W"
        ERROR = "E"

    name = models.CharField(
        "Template Name",
        max_length=64,
        primary_key=True,
    )
    category = models.CharField(
        max_length=1,
        choices=MessageCategory.choices,
        default=MessageCategory.INFO,
        verbose_name="Message Category",
    )
    subject = models.CharField(
        max_length=256,
        null=False,
        blank=False,
        help_text="The template subject / title.",
    )
    body = models.TextField(
        null=False,
        blank=False,
        help_text="The template body / content.",
    )

    def __str__(self):
        return self.name

    @classmethod
    def render_message(cls, template: str, context: dict, prefix: bool = True):
        """Helper to render a message from a DB template.

        Parameters
        ----------
        template : str
            The name of the template to use for the message.
        context : dict
            The context dict required to render the template.
        prefix : bool, optional
            If set to `True` a site-specific label will be prefixed to the subject,
            enclosed in square brackets, otherwise the subject will not be touched
            (by default True).

        Returns
        -------
        Box
            A box object containing the strings for the message category, subject,
            body, subject_raw, body_raw with the latter two having all Django
            template filters (like `naturaltime`) stripped from the template before
            rendering them. This is useful to produce identical messages independent
            of external circumstances (like the current time and so on) that can be
            used for determining if a message has been generated already before. The
            attributes of the box are:
            - `subject`
            - `body`
            - `subject_raw`
            - `body_raw`
            - `category`
        """
        if not context.get("support_contact"):
            context["support_contact"] = settings.DIOP_SUPPORT_CONTACT

        if not context.get("site_name"):
            context["site_name"] = site.name()

        if not context.get("booking_uri"):
            context["booking_uri"] = site.booking_uri()

        msg_template = cls.objects.get(pk=template)

        subj_template = msg_template.subject
        body_template = msg_template.body

        if prefix:  # prefix the subject with the site-name in square brackets
            subj_template = f"[{site.name()}] {subj_template}"

        subject = Template(subj_template).render(Context(context))
        body = Template(body_template).render(Context(context))

        pattern = re.compile(r"\| *[a-z]* *}}")
        subj_template_raw = re.sub(pattern, "}}", subj_template)
        body_template_raw = re.sub(pattern, "}}", body_template)
        subject_raw = Template(subj_template_raw).render(Context(context))
        body_raw = Template(body_template_raw).render(Context(context))

        return Box(
            {
                "subject": subject,
                "body": body,
                "subject_raw": subject_raw,
                "body_raw": body_raw,
                "category": msg_template.category,
            }
        )
