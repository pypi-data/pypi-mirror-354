"""Diop Machine model."""

from loguru import logger as log

from django.db import models

from .deliverygroup import DeliveryGroup


class Machine(models.Model):
    """Class representing details about a Diop machine."""

    fqdn = models.CharField(
        "FQDN", max_length=64, primary_key=True, help_text="Fully Qualified Domain Name"
    )
    """**CharField [PRIMARY KEY]**

    The FQDN of the machine.
    """

    deliverygroup = models.ForeignKey(
        DeliveryGroup,
        on_delete=models.CASCADE,
        verbose_name="Delivery Group",
        help_text="Delivery Group the machine belongs to.",
    )
    """**Foreign Key**

    The `diop.models.deliverygroup.DeliveryGroup` associated to the machine.
    """

    state = models.CharField(
        "Machine State",
        max_length=16,
        help_text="Current machine status.",
    )
    """**CharField**

    The current status of the machine.
    """

    powerstate = models.CharField("Power State", max_length=16)
    """**CharField**

    The current power ⚡ state of the machine.
    """

    maintenance = models.BooleanField("Maintenance Mode", default=False)
    """**BooleanField**

    Flag indicating if the machine is currently in maintenance 🔧 mode.
    """

    registration = models.CharField("Registration State", max_length=16)
    """**CharField**

    The Citrix registration state of the machine.
    """

    agent = models.CharField("Agent Version", max_length=32, null=True)
    """**CharField**

    The version of the Citrix agent running on the machine.
    """

    active = models.BooleanField(
        "Active",
        default=True,
        help_text=(
            "Indicating if the machine is active or has been retired. Entries having "
            "this set to False will be ignored by update task completeness checks."
        ),
    )
    """**BooleanField**

    Flag indicating if the machine is active or has been retired. Entries having
    this set to False will be ignored by update task completeness checks.
    """

    updated = models.BooleanField(
        "Updated",
        default=True,
        help_text=(
            "Flag tracking if the machine status is up-to-date. Has to be set to False "
            "by every function updating an entry and only re-set to True once the "
            "update has completed successfully."
        ),
    )
    """**BooleanField**

    Flag for tracking if the machine status is up-to-date.

    Has to be set to `False`by every function updating an entry and only re-set
    to `True` once the update has completed successfully.
    """

    req_maintenance = models.BooleanField(
        "Request Maintenance",
        default=False,
        help_text="Enter maintenance mode as soon as the machine is free.",
    )
    """**BooleanField**

    Flag indicating maintenance mode should be activated as soon as possible.
    """

    def __str__(self):
        """Return the`hostname()` of the machine."""
        return self.hostname

    @property
    def hostname(self):
        """The machine's hostname, i.e. its `fqdn` until the first dot (`.`)."""
        return self.fqdn.split(".")[0]

    @classmethod
    def get_or_new(cls, fqdn: str, dg_name: str, state: str = ""):
        """Get a machine object from the DB or create a new one.

        Queries the DB for an existing machine object, looking for the tuple (fqdn,
        deliverygroup), corresponding to parameters `fqdn` and `dg_name`. If no such
        entry exists, a new one will be created.

        Parameters
        ----------
        fqdn : str
            The machine's FQDN, corresponds to the **primary key** of the
            `Machine` model.
        dg_name : str
            The machine's delivery group, used as a **foreign key** to reference
            the corresponding `diop.models.deliverygroup.DeliveryGroup` record.
        state : str, optional
            An optional state to set for the machine entry. Useful when querying for
            a machine object using session information (which also contains the
            machine's state).

        Returns
        -------
        diop.models.machine.Machine
        """
        fqdn = fqdn.lower()
        log.debug(f"🖥  Checking for machine [{fqdn}]...")

        if not state:
            state = "UNKNOWN"

        d_dg, _ = DeliveryGroup.get_or_new(dg_name)

        # query for the machine, passing in "state" to be used if a new record is
        # created (see below for *updating* the state on existing machines):
        d_machine, created = cls.objects.get_or_create(
            fqdn=fqdn,
            deliverygroup=d_dg,
            defaults={
                "state": state,
            },
        )

        if created:
            log.warning(f"🖥  Creating NEW machine: [{fqdn}] ✨")
        else:
            log.debug(f"🖥  Updating existing machine: [{fqdn}] 📝")

        # if the machine exists but "state" is differing we need to update (+ save)
        if d_machine.state != state:
            d_machine.state = state
            d_machine.save()

        return d_machine, created

    @classmethod
    def from_psy_session(cls, psy_session: dict):
        """Get a Machine object from a PSyTricks session dict.

        Parameters
        ----------
        psy_session : dict
            Session infos as returned by psytricks.ResTricksWrapper.get_sessions().

        Returns
        -------
        diop.models.machine.Machine
            The DB record corresponding to the session machine.
        """
        fqdn = psy_session["DNSName"].lower()
        dg_name = psy_session["DesktopGroupName"]
        state = psy_session["MachineSummaryState"]

        d_machine, _ = cls.get_or_new(fqdn, dg_name, state)

        return d_machine
