"""Diop decorators."""

import logging
from datetime import datetime
from functools import wraps, partial
import traceback

from django.utils.timezone import make_aware

from .exceptions import UpdateMachinesError, UpdateSessionsError
from .models import Task, Issue

log = logging.getLogger(__name__)


def status_update_task(func):
    """Register a task start in the DB, execute it and check the results.

    This decorator will update the timestamp for a given "update" task start (or
    create a new one) using `func`'s name as identifier, then execute the given
    task function and watch out for exceptions.

    *WARNING*: decorated functions will have any exception "silenced" explicitly
    after adding an issue with the error details to the database.

    In case the wrapped function call succeeds, the decorator will pass on the
    resulting tuple unchanged.

    In case a known `UpdateTaskError` (or subclasses of it) exception is caught,
    the decorator will return the tuple of (`okay`, `fail`) int values, just as
    the decorated function is expected to do. Otherwise it will return (`-1`,
    `-1`) to indicate the count of updated / failed items is unknown.

    Parameters
    ----------
    func : function
        The "update" task function to be executed. It is expected to return a
        tuple of (`okay`, `fail`) int values.

    Returns
    -------
    (int, int)
        A tuple of (`okay`, `fail`) values as described above.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        task_name = f"{func.__module__}.{func.__name__}"
        log.debug(f"Starting task: {task_name}")
        try:
            d_task = Task.objects.get(name=task_name)
            d_task.t_start = make_aware(datetime.now())
        except Task.DoesNotExist:
            d_task = Task(name=task_name, t_start=make_aware(datetime.now()))

        # use the first line of the function's docstring as task description:
        d_task.description = func.__doc__.split("\n")[0]
        d_task.save()

        try:
            result = func(*args, **kwargs)

        except (UpdateMachinesError, UpdateSessionsError) as err:
            d_task.t_end = make_aware(datetime.now())
            d_task.failed += 1
            d_task.save()
            d_issue = Issue(
                severity=Issue.Level.HIGH,
                task=d_task,
                description=str(err),
            )
            log.warning(f"❗📒  Registered issue {d_issue} in DB.")
            return err.okay, err.fail

        except Exception as err:
            d_task.failed += 1
            d_task.save()
            d_issue = Issue(
                severity=Issue.Level.HIGH,
                task=d_task,
                description=str(err),
            )
            d_issue.save()
            log.warning(f"❗📒  Registered issue {d_issue} in DB.")
            return -1, -1

        log.debug(f"Completed task: {task_name}")
        d_task.t_end = make_aware(datetime.now())
        d_task.failed = 0
        d_task.save()

        return result

    return wrapper


def fire_and_dont_forget(func=None, *, severity=Issue.Level.MEDIUM):
    """Run a function silencing exceptions (adding issue records if applicable).

    The decorated "one-shot" function will be called with any exception raised
    during the function's runtime being silenced and turned into a new record
    in the Issues table.

    Parameters
    ----------
    func : function
        The "one-shot" function that should be tracked.
    severity : Issue.Level, optional
        The level to be assigned to the issue if an exception has been raised
        by the decorated function, by default `Issue.Level.MEDIUM`.
    """
    if func is None:
        return partial(fire_and_dont_forget, severity=severity)

    @wraps(func)
    def wrapper(*args, **kwargs):
        task_name = f"{func.__module__}.{func.__name__}"
        log.debug(f"Tracking one-shot function: {task_name}")

        try:
            result = func(*args, **kwargs)

        except Exception as err:
            d_issue = Issue(
                severity=severity,
                description=f"{func.__name__}: {str(err)}\n\n{traceback.format_exc()}",
            )
            d_issue.save()
            log.warning(f"❗📒  Registered issue {d_issue} in DB.")
            return None

        log.debug(f"Completed one-shot function: {task_name}")

        return result

    return wrapper
