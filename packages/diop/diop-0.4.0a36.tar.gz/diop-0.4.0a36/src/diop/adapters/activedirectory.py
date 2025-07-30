"""Adapter module to pull data from an ActiveDirectory."""

import ldap

from django.conf import settings

from box import Box
from loguru import logger as log

from ..models import User


class ActiveDirectory:
    """A connection wrapper to fetch information from an ActiveDirectory (AD).

    Attributes
    ----------
    ldap_uri : str
        The address of the LDAP / AD server to connect to.
    bind_dn : str
        The bind DN ("bind user name").
    bind_pw : str
        The bind credentials ("bind user password").
    base_dn : str
        The base DN to use as the `scope` parameter for ActiveDirectory search
        queries, for example in `get_group_members()`.
    user_details : dict
        A dict with details on user accounts queried from ActiveDirectory, with
        usernames as keys.
    ad_group : str
        The name of the AD group being used by all group-related operations.
    conn : LDAPObject
        The LDAP / AD connection object.
    """

    def __init__(
        self, bind_dn=None, bind_pw=None, ldap_uri=None, ad_group=None, base_dn=None
    ):
        """ActiveDirectory constructor.

        Parameters
        ----------
        bind_dn : str, optional
            The bind DN ("bind user name"). If not specified
            `diop_core.settings.AUTH_LDAP_BIND_DN` will be used.
        bind_pw : str, optional
            The bind credentials ("bind user password"), if not specified
            `diop_core.settings.AUTH_LDAP_BIND_PASSWORD` will be used.
        ldap_uri : str, optional
            The address of the LDAP / AD server. Will default to
            `diop_core.settings.AUTH_LDAP_SERVER_URI` if not specified.
        ad_group : str, optional
            The name of the group to get the members for. Defaults to
            `diop_core.settings.DIOP_USER_AD_GROUP` if not specified.
        base_dn : str, optional
            The base DN to use in search queries. If not given explicitly,
            `diop_core.settings.AUTH_LDAP_BASE_DN` will be used.

        Raises
        ------
        Exception
            Any exception raised during the "bind" action will be re-raised.
        """
        self.bind_dn = settings.AUTH_LDAP_BIND_DN if not bind_dn else bind_dn
        self.bind_pw = settings.AUTH_LDAP_BIND_PASSWORD if not bind_pw else bind_pw
        self.ldap_uri = settings.AUTH_LDAP_SERVER_URI if not ldap_uri else ldap_uri
        self.ad_group = settings.DIOP_USER_AD_GROUP if not ad_group else ad_group
        self.base_dn = settings.AUTH_LDAP_BASE_DN if not base_dn else base_dn

        self._ad_group_filter = "(&(objectClass=GROUP)(cn={group_name}))"
        self._ad_user_filter_person = "(&(objectClass=USER)(objectCategory=person))"

        self._group_members = []
        self._group_members_usernames = []
        self.user_details = {}

        log.debug("Setting GLOBAL LDAP options from 'AUTH_LDAP_GLOBAL_OPTIONS'...")
        for opt_name, opt_setting in settings.AUTH_LDAP_GLOBAL_OPTIONS.items():
            ldap.set_option(opt_name, opt_setting)

        log.debug(f"Trying to connect to [{self.ldap_uri}]...")
        conn = ldap.initialize(self.ldap_uri)
        conn.protocol_version = 3
        conn.set_option(ldap.OPT_REFERRALS, 0)
        try:
            conn.simple_bind_s(who=self.bind_dn, cred=self.bind_pw)
        except Exception as err:
            log.error(f"LDAP bind failed: {err}")
            raise err

        self.conn = conn
        log.debug(f"Successfully connected to [{self.ldap_uri}].")

    @property
    def group_members(self) -> list:
        """A list of user-DN's being member of the configured AD group."""
        if not self._group_members:
            self._group_members = self.get_group_members(self.ad_group)

        return self._group_members

    @property
    def group_members_usernames(self) -> list:
        """A list of usernames being member of the configured AD group."""
        if not self._group_members_usernames:
            self._group_members_usernames = self.get_group_members_usernames(
                self.group_members
            )

        return self._group_members_usernames

    def get_group_members(self, group):
        """Query the AD to retrieve a list of user-DN's being member of a group.

        If any of the DN's in the list looks like a group-DN instead of a
        user-DN (contains the sequence "Group") a recursive lookup is attempted
        by using the value of the DN's first element as the group name. In case
        the recursive lookup fails, that DN is omitted and a warning message is
        issued to the log.

        Parameters
        ----------
        group : str
            The name of the group to get the members for, e.g. `XY-VDI-Users`.

        Returns
        -------
        list(str)
            A list of user DN's.
        """
        filter = self._ad_group_filter.replace("{group_name}", group)
        result = self.conn.search_s(self.base_dn, ldap.SCOPE_SUBTREE, filter)
        raw_members = result[0][1]["member"]

        members = []
        for member in raw_members:
            try:
                # sanitize by force-decoding (assuming it is UTF-8):
                member = member.decode("utf-8")
            except:
                pass

            if "Group" not in member:
                members.append(member)
                continue

            log.debug(f"Potential group: {member}")
            try:
                group_name = member.split(",")[0].split("=")[1]
                members += self.get_group_members(group_name)
            except Exception as err:
                log.warning(f"Unable to resolve [{member}]: {err}")

        log.debug(f"Got {len(members)} members for group [{group}].")
        return members

    def get_group_members_usernames(self, group_members_dn) -> list:
        """Fetch usernames for the given list of group member DN's.

        Parameters
        ----------
        group_members_dn : list(str)
            The group members DN's to fetch the usernames for.

        Returns
        -------
        list
        """
        usernames = []
        for user_dn in group_members_dn:
            details = self.user_details_from_dn(user_dn)
            if details:
                usernames.append(details.username)
        log.debug(f"Got {len(usernames)} usernames.")
        return usernames

    def user_details_from_dn(self, user_dn) -> Box:
        """Fetch display name, email and department for a user DN.

        Parameters
        ----------
        user_dn : str or str-like
            The user-DN to fetch details for.

        Returns
        -------
        Box
            A Box with the attributes listed below, or `None` in case the lookup
            failed:

            - `username` : str
            - `display_name` : str
            - `email` : str
            - `department` : str
            - `enabled` : bool
        """
        try:
            # sanitize by force-decoding (assuming it is UTF-8):
            user_dn = user_dn.decode("utf-8")
        except:
            pass

        log.debug(f"Getting details for [{user_dn}]...")
        result = self.conn.search_s(
            user_dn, ldap.SCOPE_BASE, self._ad_user_filter_person
        )
        if len(result) < 1:
            log.warning(f"No results for user DN [{user_dn}]!")
            return None

        if len(result) > 1:
            log.error(f"Huh?! Got multiple results for user DN [{user_dn}]!")
            return None

        details = result[0][1]
        display_name = details["displayName"][0].decode("utf-8")
        email = details["mail"][0].decode("utf-8")
        username = details["sAMAccountName"][0].decode("utf-8")
        user_account_control = details["userAccountControl"][0].decode("utf-8")
        enabled = True if not int(user_account_control) & 0x002 else False
        try:
            department = details["department"][0].decode("utf-8")
        except:  # ruff: noqa: E722 (bare-except)
            department = ""

        details = Box(
            {
                "username": username,
                "display_name": display_name,
                "email": email,
                "department": department,
                "enabled": enabled,
            }
        )
        # store in the object's dict `user_details` using `username` as the key:
        self.user_details[username] = details

        return details
