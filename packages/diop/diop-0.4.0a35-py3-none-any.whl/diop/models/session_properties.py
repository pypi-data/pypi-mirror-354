"""Diop SessionProperties model."""

from datetime import datetime

from loguru import logger as log

from django.db import models
from django.utils.timezone import make_aware

from .session import Session


class SessionProperties(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, verbose_name="Session UID"
    )
    t_change = models.DateTimeField(
        "State Change Time",
        help_text="Citrix:SessionStateChangeTime",
    )
    state = models.CharField("Session State", max_length=16)
    client_address = models.CharField(
        "Client IP",
        max_length=46,
        help_text="IP address of the client currently (or last) connected.",
    )
    client_name = models.CharField(
        "Client Name",
        max_length=64,
        help_text="The name of the client currently (or last) connected.",
    )
    client_version = models.CharField(
        "Client Version",
        max_length=16,
        help_text="The version of the client currently (or last) connected.",
    )

    class Meta:
        verbose_name = "Session Properties"
        verbose_name_plural = "Session Properties"
        constraints: [
            models.UniqueConstraint(
                fields=["t_change", "state"],
                name="unique_tchange_state_combination",
            )
        ]

    def __str__(self):
        return f"({self.session}) {str(self.t_change)} [{self.state}]"

    @classmethod
    def get_or_new(
        cls,
        session: Session,
        t_change: datetime,
        state: str,
        defaults: dict = {},
    ):
        """Get a SessionProperties object from the DB or create a new one.

        Query the DB for an existing session object looking for the tuple
        (session, t_change, state) or create one if nothing is found.

        Note that the method is intentionally NOT called `get_or_create` to
        lower the risk of mixing it up with Django's built-in model manager one.

        Parameters
        ----------
        session: Session
            The Session to which this object belongs.
        t_change: datetime
        state: str

        Returns
        -------
        (properties, created) : (diop.models.SessionProperties, bool)
        """
        props, created = SessionProperties.objects.get_or_create(
            session=session,
            t_change=make_aware(t_change),
            state=state,
            defaults=defaults,
        )

        # only if the session properties entry was newly created we need to fill
        # in the details, otherwise we can simply return here:
        if created:
            log.success(f"✨🎬🏷 Created NEW session properties: {props}")
        else:
            log.debug(f"🎬🏷 Session properties known, not updating: {props} 🆗")

        return props, created
