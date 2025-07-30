"""Diop PpmsBooking model."""

from datetime import timedelta, datetime, time

from loguru import logger as log

from django.db import models
from django.utils.timezone import make_aware

from ..utils import naive_minutes
from .reservation import Reservation


class PpmsBooking(models.Model):
    class Meta:
        verbose_name = "PPMS Booking"
        constraints = [
            models.UniqueConstraint(
                fields=["username", "system_id", "t_start", "t_end"],
                name="unique_booking",
            )
        ]

    class SyncState(models.TextChoices):
        DELETED = "D"
        NEW = "N"
        KNOWN = "K"

    # NOTE: username is NOT a FK - it stores the data just as returned by PPMS
    username = models.CharField(max_length=32, verbose_name="PPMS Username")
    system_id = models.IntegerField("PPMS System ID")
    t_start = models.DateTimeField("Booking Start", null=False, blank=False)
    t_end = models.DateTimeField("Booking End", null=False, blank=False)
    ppms_session = models.CharField(
        "PPMS Session ID", max_length=8, null=True, blank=True
    )
    sync_state = models.CharField(
        max_length=1,
        choices=SyncState.choices,
        default=SyncState.NEW,
    )
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        help_text="Reservation to which this booking belongs.",
        null=True,
        blank=True,
    )

    def __str__(self):
        return (
            f"({self.pk}) {self.username}@{self.system_id} "
            f"[{naive_minutes(self.t_start)} -- {naive_minutes(self.t_end)}]"
        )

    @classmethod
    def mark_all_deleted(cls, date):
        """Set `sync_state` to `D` for all bookings on the given day.

        Parameters
        ----------
        date : datetime.datetime
            The date for which the `sync_state` should be set to "deleted".
        """
        date = datetime.combine(date, time.min)
        t0 = make_aware(date)
        t1 = make_aware(date + timedelta(days=1))
        log.debug(f"Setting bookings to DELETED from [{t0}] to [{t1}].")
        cls.objects.filter(t_start__gte=t0, t_end__lte=t1).update(sync_state="D")
