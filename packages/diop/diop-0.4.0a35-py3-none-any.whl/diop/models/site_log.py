"""Diop SiteLog model."""

from django.db import models

from .user import User
from .deliverygroup import DeliveryGroup
from .machine import Machine
from .session import Session
from .task import Task
from .notification import Notification
from .reservation import Reservation


class SiteLog(models.Model):
    """Log entries of status changes, action requests and such.

    Entries in this table will reflect the site's history with status changes of
    sessions and machines, notifications, force-disconnects, force-terminates
    and more.
    """

    class Meta:
        verbose_name = "Site Log"

    name = models.CharField("Name", max_length=128)
    parameters = models.CharField("Parameters", max_length=512)
    time = models.DateTimeField(
        auto_now_add=True,
        help_text="Time the action was triggered.",
    )
    details = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    deliverygroup = models.ForeignKey(
        DeliveryGroup, on_delete=models.SET_NULL, null=True, blank=True
    )
    machine = models.ForeignKey(
        Machine, on_delete=models.SET_NULL, null=True, blank=True
    )
    session = models.ForeignKey(
        Session, on_delete=models.SET_NULL, null=True, blank=True
    )
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)
    notification = models.ForeignKey(
        Notification, on_delete=models.SET_NULL, null=True, blank=True
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.SET_NULL, null=True, blank=True
    )
