"""Diop Issue model."""

from django.db import models
from django.utils.timezone import make_naive

from loguru import logger as log

from .task import Task
from .user import User


class Issue(models.Model):
    class Level(models.IntegerChoices):
        LOW = 0, "Low"
        MEDIUM = 1, "Medium"
        HIGH = 2, "High"
        CRITICAL = 3, "Critical"
        MELTDOWN = 4, "Meltdown"

    severity = models.SmallIntegerField(
        default=0,
        choices=Level.choices,
        help_text="Values from 0 to 4, higher means more critical.",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="Time the issue occurred.",
    )
    resolved = models.BooleanField(
        default=False,
        help_text="Flag indicating the issue is resolved.",
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        help_text="Related task causing the issue (if applicable).",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="Related user (if applicable).",
        null=True,
        blank=True,
    )
    description = models.TextField()

    def __str__(self):
        severity = self.get_severity_display()
        timestamp = self.timestamp
        try:
            timestamp = make_naive(self.timestamp).strftime("%H:%M:%S")
        except Exception as err:
            log.error(f"Failed to format timestamp [{timestamp}]: {err}")
        user = f", user=[{self.user.username}]" if self.user else ""
        task = f", task=[{self.task.short}]" if self.task else ""

        return f"#{self.id} [{severity}] ({timestamp}){user}{task}"
