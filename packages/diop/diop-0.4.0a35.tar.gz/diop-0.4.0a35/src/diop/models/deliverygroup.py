"""Diop DeliveryGroup model."""

from loguru import logger as log

from django.db import models

from .user import User


class DeliveryGroup(models.Model):
    dg_name = models.CharField(
        "Group Name",
        max_length=32,
        primary_key=True,
        help_text="Name of the Delivery Group (DG).",
    )
    host_prefix = models.CharField(
        "Hostname Prefix",
        max_length=32,
        help_text=(
            "Hostnames starting with this prefix will be considered "
            "members of the DG."
        ),
        default="",
        blank=True,
    )
    booking_required = models.BooleanField(
        "Booking Required",
        default=False,
        help_text="Sessions in this DG require a valid booking.",
    )
    access_users = models.ManyToManyField(
        to=User,
        blank=True,
        help_text="Users that are explicitly granted access to this DG.",
    )
    unique_session = models.BooleanField(
        default=True,
        help_text=(
            "Allow only one session per user across *ALL* groups having this "
            "flag enabled (enforced via a housekeeping task)."
        ),
    )

    class Meta:
        verbose_name = "Delivery Group"

    def __str__(self):
        return self.dg_name

    @classmethod
    def get_or_new(cls, dg_name: str):
        """Get a DG from the DB or create a new one if it doesn't exist.

        Parameters
        ----------
        dg_name : str
            The name of the delivery group.

        Returns
        -------
        diop.models.DeliveryGroup, bool
            A tuple consisting of the delivery group DB record and a boolean flag
            indicating if the record has been newly created.
        """
        log.debug(f"💫 Checking for delivery group: {dg_name}")
        d_dg, created = cls.objects.get_or_create(dg_name=dg_name)
        if created:
            log.warning(f"💫 Created NEW delivery group: [{d_dg}] ✨")
        else:
            log.debug(f"💫 Using existing DG [{d_dg}] 🆗")
        return d_dg, created
