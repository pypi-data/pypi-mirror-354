"""Diop Session model."""

from datetime import timedelta

from loguru import logger as log

from django.db import models
from django.utils.timezone import make_aware, now

from .machine import Machine
from .user import User


class Session(models.Model):
    """Class representing details about a Diop session."""

    uid = models.BigIntegerField(
        "Session UID",
        primary_key=True,
        help_text="Citrix:Uid (session identifier)",
    )
    """**BigIntegerField [PRIMARY KEY]**

    The *Session UID* as given by Citrix / CVAD.
    """

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        verbose_name="Machine",
        help_text="Machine associated to the session",
    )
    """**Foreign Key**

    The `diop.models.machine.Machine` associated to the session.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="User",
        null=True,
        blank=True,
        help_text="User associated to the session, can be empty!",
    )
    """**Foreign Key**

    The `diop.models.user.User` associated to the session, **may be empty!**
    """

    t_start = models.DateTimeField(
        "Start Time", help_text="Citrix:StartTime (session start timestamp)"
    )
    """**DateTimeField**

    The session start time as provided by Citrix / CVAD.
    """

    t_end = models.DateTimeField(
        "End Time",
        null=True,
        blank=True,
        help_text="Timestamp when the end of the session was detected first.",
    )
    """**DateTimeField**

    The timestamp when the end of the session was detected by Diop.

    **Important:** this information is **derived** by Diop, as it is **not
    provided by Citrix / CVAD** (at least not reliably)!
    """

    updated = models.BooleanField(
        "Updated",
        default=True,
        help_text=(
            "Flag tracking if the session status is up-to-date. Has to be set to False "
            "by every function updating an entry and only re-set to True once the "
            "update has completed successfully."
        ),
    )
    """**BooleanField**

    Flag tracking if the session status is up-to-date. Must be set to `False` by
    every function updating an entry and only re-set to `True` once the update
    has completed successfully.
    """

    def __str__(self):
        """Get a string representation of the session."""
        username = "-"
        if self.user:
            username = self.user.username
        return f"{str(self.uid)} [{username}]"

    @property
    def cur_properties(self):
        """Get the newest session properties record of this session.

        Returns
        -------
        diop.models.session_properties.SessionProperties
        """
        return self.sessionproperties_set.order_by("t_change").last()

    @property
    def cur_state(self):
        """Get the *state* of this session record.

        Returns
        -------
        str
            Either the string `ended` in case this session record's `t_end` is
            not empty, or otherwise the state of the last corresponding record
            in `diop.models.session_properties.SessionProperties.state`.
        """
        if self.t_end:
            return "ended"

        return self.sessionproperties_set.order_by("t_change").last().state

    @property
    def disconnected_since(self):
        """Number of seconds since the session is in "disconnected" state.

        Returns
        -------
        int
            The number of seconds since the session was disconnected, or -1 in
            case the session is active.
        """
        session_props = self.cur_properties
        if session_props.state != "disconnected":
            return -1

        delta = int((now() - session_props.t_change).total_seconds())
        log.trace(f"Session [{self}] is disconnected since {delta}s")

        return delta

    @property
    def prospected_termination(self):
        """Expected termination timepoint for disconnected sessions.

        Please note that this does NOT take into account the actual state of the
        session, it simply adds the user-specific "disconnected_max" timespan to
        the last session status change.

        Returns
        -------
        datetime.datetime
        """
        return self.cur_properties.t_change + timedelta(
            hours=self.user.disconnected_max
        )

    @property
    def is_subject_to_disconnected_termination(self):
        """The related user has disconnected-session-termination enabled."""
        return self.user.disconnected_max > 0

    @property
    def exceeds_disconnected_limit(self):
        """The session's disconnection time exceeds the related user's limit."""
        limit = self.user.disconnected_max * 60 * 60
        if limit <= 0:
            return False

        if self.disconnected_since > limit:
            return True

        return False

    @classmethod
    def is_up_to_date(cls, psy_session):
        """Update (or create) session details from a PSyTricks session dict.

        Parameters
        ----------
        psy_session : dict
            A dict with session details as returned by
            `psytricks.wrapper.ResTricksWrapper.get_sessions()`.

        Returns
        -------
        session, created : diop.models.Session, bool
            A tuple with the first element being the Diop session record and the
            second one being a boolean indicating if the record has been newly
            created (`True`) or if an existing record was updated (`False`).
        """
        uid = psy_session["Uid"]
        session, created = Session.get_or_new(
            uid=uid,
            machine=Machine.from_psy_session(psy_session),
            user=User.from_psy_session(psy_session),
            t_start=psy_session["StartTime"],
        )

        # set the `updated` state without triggering post-save signals or similar:
        Session.objects.filter(uid=uid).update(updated=True)

        return session, created

    @classmethod
    def get_or_new(cls, uid, machine, user, t_start):
        """Get a Session object from the DB or create a new one.

        Query the DB for an existing session object looking for the tuple (UID,
        FQDN, username, session start) or create one if nothing is found.

        Note that the method is intentionally NOT called `get_or_create` to
        lower the risk of mixing it up with Django's built-in model manager one.

        Parameters
        ----------
        uid : int
            The session UID.
        machine : Machine
            The Machine object (or FQDN string).
        user : User
            The user object.
        t_start : datetime
            The session start timestamp.

        Returns
        -------
        (session, created) : (diop.models.Session, bool)
        """
        d_session, created = Session.objects.get_or_create(
            uid=uid,
            machine=machine,
            user=user,
            t_start=make_aware(t_start),
        )
        if created:
            log.success(f"✨🎬 Created NEW session entry: {d_session}")
        else:
            log.debug(f"🎬 Session already known to DB: {d_session} 🆗")
        return d_session, created

    @classmethod
    def last_completed(cls, dg, user):
        """Get the last completed session of a user in the given delivery group.

        Query the DB for all session of the given user in the specified DG and
        return the last one that is already completed / finished.

        Parameters
        ----------
        dg : DeliveryGroup
            The DG to which the session belongs.
        user : User
            The session user.accessgroup_member

        Returns
        -------
        Session
        """
        session = (
            Session.objects.filter(
                user=user, machine__deliverygroup=dg, t_end__isnull=False
            )
            .order_by("-t_end")
            .first()
        )

        return session
