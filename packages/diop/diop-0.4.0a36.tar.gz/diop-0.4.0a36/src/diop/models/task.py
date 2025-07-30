"""Diop Task model."""

from django.db import models
from django.utils.timezone import now


class Task(models.Model):
    name = models.CharField("Task Name", max_length=128, primary_key=True)
    # NOTE: it is on purpose that `t_start` is not using `auto_now_add` since this
    # allows to set the start timestamp explicitly - this is needed when a task is
    # started again at a later point (which is standard behavior):
    t_start = models.DateTimeField("Start Time", default=now)
    t_end = models.DateTimeField(
        "End Time",
        null=True,
        blank=True,
        help_text="Empty if task is still running or did not succeed.",
    )
    unfinished = models.SmallIntegerField(
        default=0,
        help_text="Counter on previous unfinished runs when next one tries to start.",
    )
    failed = models.SmallIntegerField(
        default=0, help_text="Counter on previously failed attempts."
    )
    description = models.TextField(null=False, blank=True)

    def __str__(self):
        return self.name

    @property
    def short(self):
        """Return the 'short' task name, i.e. everything following the last dot.

        Returns
        -------
        str
        """
        return self.name.split(".")[-1]
