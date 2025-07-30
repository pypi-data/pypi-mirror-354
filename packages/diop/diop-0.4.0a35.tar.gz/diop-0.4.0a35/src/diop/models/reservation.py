"""Diop Reservation model."""

from datetime import timedelta
from datetimerange import DateTimeRange

from django.db import models
from django.utils import timezone

from ..utils import naive_minutes
from .user import User
from .deliverygroup import DeliveryGroup


class Reservation(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "deliverygroup", "t_start", "t_end"],
                name="unique_reservation",
            )
        ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deliverygroup = models.ForeignKey(
        DeliveryGroup,
        on_delete=models.CASCADE,
        verbose_name="Delivery Group",
        help_text="Delivery Group the reservation is for.",
    )
    t_start = models.DateTimeField("Reservation Start", null=False, blank=False)
    t_end = models.DateTimeField("Reservation End", null=False, blank=False)

    def __str__(self):
        return (
            f"({self.pk}) {self.user.username}@{self.deliverygroup} "
            f"[{naive_minutes(self.t_start)} -- {naive_minutes(self.t_end)}]"
        )

    @property
    def t_range(self):
        return DateTimeRange(self.t_start, self.t_end)

    @property
    def till_end(self):
        """The number of seconds until the end of the reservation.

        Returns
        -------
        float
            The time (in seconds) that is left until the reservation ends, will
            be negative if the reservation's end is in the past.
        """
        return (self.t_end - timezone.now()).total_seconds()

    @property
    def since_start(self):
        """The number of seconds since the start of the reservation.

        Returns
        -------
        float
            The time (in seconds) that has passed since the reservation's start,
            will be negative if the start time is in the future.
        """
        return (timezone.now() - self.t_start).total_seconds()

    @classmethod
    def running(cls, dg_name):
        """The currently active ("running") reservations for the given DG.

        Parameters
        ----------
        dg_name : str
            The name of the delivery group to check reservations for.

        Returns
        -------
        QuerySet
            All reservations whose starttime is in the past and endtime is in
            the future (both also including "now").
        """
        now = timezone.now()
        return cls.objects.filter(
            deliverygroup__dg_name=dg_name, t_start__lte=now, t_end__gte=now
        )

    @classmethod
    def running_usernames(cls, dg_name):
        """A list of usernames having currently active ("running") reservations.

        Parameters
        ----------
        dg_name : str
            The name of the delivery group to check reservations for.

        Returns
        -------
        QuerySet
            All usernames having a currently active reservation as given by
            `Reservation.running()`.
        """
        running = cls.running(dg_name)
        return running.values_list("user__username", flat=True)

    @classmethod
    def ending_in_less_than(cls, minutes: int, dg_name: str, username: str = ""):
        """Running reservations ending in less than the given delta from now.

        Parameters
        ----------
        minutes : int
            The amount of minutes to use as the limit for checking when the
            reservations will expire.
        dg_name : str
            The name of the delivery group to check reservations for.
        username : str, optional
            An optional username to filter the reservations for, by default ""
            which will result in no filtering being done.

        Returns
        -------
        QuerySet
            All running reservations belonging to the given DG that will expire
            in less than the given number of minutes, optionally restricted by
            the username (if given).
        """
        running = cls.running(dg_name)
        ending = running.filter(
            t_end__lte=(timezone.now() + timedelta(minutes=minutes))
        )
        if not username:
            return ending

        return ending.filter(user__username=username)
