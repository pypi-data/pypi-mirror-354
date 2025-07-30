"""Diop User model."""

from loguru import logger as log

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=32, primary_key=True)
    fullname = models.CharField(
        max_length=128,
        verbose_name="Full Name",
        help_text='LDAP attribute "displayName".',
        null=True,
        blank=True,
    )
    groupname = models.CharField(
        max_length=128,
        verbose_name="Group Name",
        help_text="Manually set (cannot be derived reliably via LDAP).",
        null=True,
        blank=True,
    )
    department = models.CharField(
        max_length=128,
        help_text=(
            'LDAP attribute "department" (may be set manually but LDAP has '
            "priority in case the field is present there)."
        ),
        null=True,
        blank=True,
    )
    email = models.CharField(max_length=128)
    ppms_group = models.CharField(
        max_length=64,
        verbose_name="PPMS Group",
        null=True,
        blank=True,
    )
    ppms_fullname = models.CharField(
        max_length=128,
        verbose_name="PPMS Full Name",
        null=True,
        blank=True,
    )
    gracetime = models.IntegerField(
        default=0, help_text="Number of days until data expires on the storage."
    )
    disconnected_max = models.IntegerField(
        verbose_name="Max. disconnected hours.",
        default=0,
        help_text=(
            "Hours after which a disconnected session is terminated, negative values "
            "mean no session termination will be enforced."
        ),
    )
    enabled = models.BooleanField(
        default=True,
        help_text="Account is enabled in AD (2nd bit of `userAccountControl` is 0).",
    )
    accessgroup_member = models.BooleanField(
        default=False,
        help_text="User is in the AD-group permitting platform access.",
    )

    def __str__(self):
        """The "local" part of the user's email.

        If the domain part contains something else than the configured site
        domain, that part is added as well.
        """
        # TODO: introduce setting DIOP_DOMAIN setting and adjust logic accordingly!
        mailname = self.email
        try:
            mailname, domain = self.email.split("@")
            if domain.startswith("stud"):
                mailname += " (s)"
        except:
            pass

        return mailname

    @property
    def full_details(self):
        return (
            f"username: {self.username}\n"
            f"fullname: {self.fullname}\n"
            f"groupname: {self.groupname}\n"
            f"department: {self.department}\n"
            f"email: {self.email}\n"
            f"ppms_group: {self.ppms_group}\n"
            f"ppms_fullname: {self.ppms_fullname}\n"
            f"gracetime: {self.gracetime}\n"
            f"disconnected_max: {self.disconnected_max}\n"
            f"enabled: {self.enabled}\n"
            f"accessgroup_member: {self.accessgroup_member}\n"
        )

    @classmethod
    def get_or_new(cls, username: str, defaults: dict = {}):
        r"""Get a user record from the DB or create one if it doesn't exist.

        Note that the method is intentionally NOT called `get_or_create` to
        lower the risk of mixing it up with Django's built-in model manager one.

        Parameters
        ----------
        username : str
            The username. Any leading prefix up to a `\` (backslash) will be
            silently stripped (e.g. `NTDOMAIN\foo` will become `foo`).
        defaults : dict, optional
            A dict with defaults being passed to the `get_or_create()` call.
            The values in the dict will _not_ be used for the record lookup, but
            will be used in case a new one has to be created.

        Returns
        -------
        diop.models.User, bool
            A tuple consisting of the user DB record and a boolean flag
            indicating if the record has been newly created.
        """
        username = username.lower()
        try:
            username = username.split("\\")[1]
        except:  # ruff: noqa: E722
            pass  # if the split fails we're using the string as-is

        log.debug(f"👩‍🔬 Checking for user [{username}]...")

        d_user, created = cls.objects.get_or_create(
            username=username,
            defaults=defaults,
        )

        if created:
            log.success(f"👩‍🔬 Created NEW user entry: [{d_user.username}] ✨")
        else:
            log.debug(f"👩‍🔬 User already known: [{d_user.username}] 🆗")

        return d_user, created

    @classmethod
    def is_up_to_date_from_ad(cls, user_details, accessgroup_member):
        """Create or update a user from an AD query response.

        Parameters
        ----------
        user_details : Bix
            A Box object with user details as returned by
            `diop.adapters.activedirectory.ActiveDirectory.user_details_from_dn`.
        accessgroup_member : bool
            A flag indicating whether the user is a member of the access group.

        Returns
        -------
        (created, updated) : (bool, bool)
            A tuple indiciating if the user record has been created or updated.
        """
        return cls.is_up_to_date(
            username=user_details.username,
            email=user_details.email,
            fullname=user_details.display_name,
            department=user_details.department,
            enabled=user_details.enabled,
            accessgroup_member=accessgroup_member,
        )

    @classmethod
    def is_up_to_date(
        cls, username, email, fullname, department, enabled, accessgroup_member
    ):
        """Create or get a user record, ensuring all attributes are up-to-date.

        Fetch an existing user record (identified via the PK `username`) or
        create a new record using the given details. In case an existing record
        is found, it is made sure the non-PK attributes match the ones given as
        parameters to this method.

        Parameters
        ----------
        username : str
            The username (=primary key).
        email : str
            The user's email address.
        fullname : str
            The full name.
        department : str
            The department
        enabled : bool
            A flag indicating if the user account is enabled in ActiveDirectory.
        accessgroup_member : bool
            A flag indicating whether the user is a member of the access group.

        Returns
        -------
        (created, updated) : (bool, bool)
            A tuple indiciating if the user record has been created or updated.
        """
        updated = False
        defaults = {
            "email": email,
            "fullname": fullname,
            "department": department,
            "enabled": enabled,
            "accessgroup_member": accessgroup_member,
        }
        d_user, created = cls.get_or_new(username=username, defaults=defaults)

        if created or (
            d_user.email == email
            and d_user.fullname == fullname
            and d_user.department == department
            and d_user.enabled == enabled
            and d_user.accessgroup_member
        ):
            log.debug(f"👩‍🔬 No further user changes: [{d_user.username}] 🆗")
            return created, updated

        updated = True
        d_user.email = email
        d_user.fullname = fullname
        d_user.department = department
        d_user.enabled = enabled
        # TODO: why us `True` hardcoded here for the accessgroup_member, is this
        # a bug? If not, explain it here (and in the docstring)!
        d_user.accessgroup_member = True
        d_user.save()

        return created, updated

    @classmethod
    def from_psy_session(cls, psy_session: dict):
        """Get a DIOP user object from a PSyTricks session dict.

        Parameters
        ----------
        psy_session : dict
            Session infos as returned by psytricks.ResTricksWrapper.get_sessions().

        Returns
        -------
        diop.models.User
            The DB record corresponding to the session user.
        """
        username = psy_session["UserName"]
        upn = psy_session["UserUPN"]

        d_user, _ = cls.get_or_new(username, defaults={"email": upn})

        return d_user
