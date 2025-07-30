"""Custom management command for registering schdeuled tasks."""

from datetime import datetime, timedelta

from django.db import IntegrityError
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from django_q.models import Schedule


def next_time_at(hour, minute=0):
    """Get the next timezone-aware timepoint with given hour / minute.

    The function is creating a timezone-aware `datetime` object with the given
    `hour` and `minute` (all smaller components will be set to zero), making it
    the closest one that is still in the future.

    Meaning if that time has not yet passed today, the returned object will
    represent a timepoint of today, otherwise of tomorrow.

    Parameters
    ----------
    hour : int
        The hour for the timepoint.
    minute : int, optional
        The minute for the timepoint, by default 0.

    Returns
    -------
    datetime
    """
    tp = timezone.make_aware(
        datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    )
    if tp < timezone.now():
        tp = tp + timedelta(days=1)

    return tp


class Command(BaseCommand):
    """Management command to register default Diop tasks in the scheduler."""

    help = "Register standard tasks in the scheduler"

    @staticmethod
    def remove_task(name):
        """Remove a task with the given name from the scheduler.

        Parameters
        ----------
        name : str
            The name of the task to be removed.
        """
        deleted, _ = Schedule.objects.filter(name=name).delete()
        if deleted:
            print(f"Removed task: '{name}'")

    @staticmethod
    def add_task_unless_existing(
        name,
        func,
        hook=None,
        args=None,
        kwargs=None,
        schedule_type=Schedule.ONCE,
        minutes=None,
        repeats=-1,
        next_run=timezone.now(),
        cron=None,
        cluster=None,
        intended_date_kwarg=None,
    ):
        """Add a task unless the Schedule already has one with the same name."""
        if Schedule.objects.filter(name=name).exists():
            print(f"Task already existing: '{name}'")
            return

        print(f"Registering new task: '{name}' ...")
        schedule = Schedule(
            name=name,
            func=func,
            hook=hook,
            args=args,
            kwargs=kwargs,
            schedule_type=schedule_type,
            minutes=minutes,
            repeats=repeats,
            next_run=next_run,
            cron=cron,
            cluster=cluster,
            intended_date_kwarg=intended_date_kwarg,
        )
        # trigger validation of the schedule
        schedule.full_clean()
        schedule.save()
        print(f"✅ Done registering new task: '{name}'")

    def handle(self, *args, **options):
        """Perform all task registrations in the scheduler.

        Any task is registered by first removing it from the scheduler and then
        re-adding it with the parameters defined here. This ensures that
        changing parameters here will update the corresponding tasks in the
        scheduler as well.

        Note
        ----
        Subclasses of `BaseCommand` must override their `handle` method. The
        method is called automatically after the Django environment has been
        configured and the CLI arguments have been parsed.
        """
        Command.remove_task(name="PPMS: Pull Users (Fast)")
        Command.add_task_unless_existing(
            func="diop.tasks.pull_ppms_users",
            name="PPMS - Pull Users Fast (@1m)",
            schedule_type=Schedule.MINUTES,
            minutes=1,
            cluster="ppms-short",
        )

        Command.remove_task(name="PPMS: Pull Users (Force-Refresh)")
        Command.add_task_unless_existing(
            func="diop.tasks.pull_ppms_users",
            name="PPMS - Pull Users Force-Refresh (@1h)",
            schedule_type=Schedule.HOURLY,
            cluster="ppms-long",
            kwargs={"force_refresh": True},
        )

        Command.remove_task(name="PPMS: Pull Bookings (2d)")
        Command.add_task_unless_existing(
            func="diop.tasks.pull_ppms_bookings",
            name="PPMS - Pull Bookings next 2d (@1m)",
            schedule_type=Schedule.MINUTES,
            minutes=1,
            cluster="ppms-short",
            kwargs={"days": 2},
        )

        Command.remove_task(name="PPMS: Pull Bookings (10d)")
        Command.add_task_unless_existing(
            func="diop.tasks.pull_ppms_bookings",
            name="PPMS - Pull Bookings next 10d (@1h)",
            schedule_type=Schedule.HOURLY,
            cluster="ppms-short",
            kwargs={"days": 10},
        )

        Command.remove_task(name="ActiveDirectory: Pull User Details")
        Command.add_task_unless_existing(
            func="diop.tasks.update_users_from_ad",
            name="ActiveDirectory - Pull User Details (@1h)",
            schedule_type=Schedule.HOURLY,
            cluster="activedirectory",
        )

        Command.remove_task(name="Housekeeping: @1m")
        Command.add_task_unless_existing(
            func="diop.tasks.housekeeping_every_minute",
            name="Housekeeping - Constantly (@1m)",
            schedule_type=Schedule.MINUTES,
            minutes=1,
            cluster="housekeeping",
        )

        Command.remove_task(name="Housekeeping: Day Start")
        Command.add_task_unless_existing(
            func="diop.tasks.housekeeping_start_of_day",
            name="Housekeeping - Day Start (09:00)",
            schedule_type=Schedule.DAILY,
            cluster="housekeeping",
            next_run=next_time_at(9),
        )

        Command.remove_task(name="Update Machines (@1m)")
        Command.add_task_unless_existing(
            func="diop.tasks.update_machine_status",
            name="Citrix - Pull Machine Status (@1m)",
            schedule_type=Schedule.MINUTES,
            minutes=1,
            cluster="statusupdates",
        )

        Command.remove_task(name="Update Sessions (@1m)")
        Command.add_task_unless_existing(
            func="diop.tasks.update_session_status",
            name="Citrix - Pull Session Status (@1m)",
            schedule_type=Schedule.MINUTES,
            minutes=1,
            cluster="statusupdates",
        )

        Command.remove_task(name="Disconnect Sessions")
        Command.add_task_unless_existing(
            func="diop.tasks.housekeeping_start_of_day",
            name="Housekeeping - Early Morning (04:00)",
            schedule_type=Schedule.DAILY,
            cluster="housekeeping",
            next_run=next_time_at(4),
        )
