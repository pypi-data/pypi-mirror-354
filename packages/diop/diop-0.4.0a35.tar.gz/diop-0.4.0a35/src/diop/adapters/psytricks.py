"""Adapter module to work with PSyTricks data."""

from os import environ

from loguru import logger as log
from psytricks.wrapper import ResTricksWrapper

from django.conf import settings
from django.utils.functional import LazyObject

from .. import site
from ..models import Machine, Session, SessionProperties, SiteLog, User, DeliveryGroup


class ResTricksClient(LazyObject):
    """LazyObject wrapper for the ResTricksWrapper class.

    By encapsulating the psytricks.wrapper.ResTricksWrapper in a LazyObject,
    instantiation of the object is deferred until its first actual usage.
    """

    def _setup(self):
        if "PDOC_DISPLAY_ENV_VARS" in environ.keys():
            # do NOT instantiate the wrapper if the code is only being processed
            # by pdoc (using the `PDOC_DISPLAY_ENV_VARS` environment variable
            # as an indicator)
            return

        log.debug("Instantiating ResTricksClient...")
        self._wrapped = ResTricksWrapper(
            base_url=settings.PSYTRICKS_BASE_URL,
            verify=settings.PSYTRICKS_VERIFY,
            lazy=True,
        )
        if settings.DIOP_DRY_RUN:
            self._wrapped.read_only = True


broker = ResTricksClient()


def process_session_info(psy_session: dict):
    """Update the DB on sessions and its properties from a session details dict.

    Parameters
    ----------
    psy_session : dict
        A dict with session details as returned by
        `psytricks.wrapper.ResTricksWrapper.get_sessions()`.

    Returns
    -------
    bool, bool
        A tuple of boolean values indicating if a new session record (1st
        element) or a new session properties record (2nd element) has been
        created from the session details.
    """
    # log.warning(psy_session)

    # FIXME: sometimes Citrix returns "partial" sessions for currently unknown
    # reasons, which won't contain all the details - resulting in an exception
    # being raised. Rather have a proper session object in the psytricks package
    # (e.g. that has an attribute `.valid` or similar) and use that one here
    # than blindly accessing dict fields that may not exist!

    d_session, created_s = Session.is_up_to_date(psy_session)

    defaults = {
        "client_address": psy_session["ClientAddress"],
        "client_name": psy_session["ClientName"],
        "client_version": psy_session["ClientVersion"],
    }

    d_session_props, created_p = SessionProperties.get_or_new(
        session=d_session,
        t_change=psy_session["SessionStateChangeTime"],
        state=psy_session["SessionState"],
        defaults=defaults,
    )

    log.debug(f"🎬✅ DONE updating details on [{d_session}]")
    return created_s, created_p


def process_machine_info(psy_machine: dict):
    """Update the DB on machine properties from a machine details dict.

    Machines having an empty attribute `DesktopGroupName` will be skipped (with
    a warning log message being issued), as they are not assigned to a Delivery
    Group and hence would lead to confusing results in the Diop DB. This may
    happen e.g. when setting up new VMs that are already registered with the
    broker, but not yet assigned to a Delivery Group.

    Parameters
    ----------
    psy_machine : dict
        A dict with machine details as returned by
        `psytricks.wrapper.ResTricksWrapper.get_machine_status()`
    """
    # FIXME: currently only machine dicts that have an empty DesktopGroupName
    # are treated specially (skipped), however it is not fully clear if other
    # "incomplete" machine dicts might be produced by the broker - in case this
    # happens, see the note about incomplete details in `process_session_info`
    # and go for a similar strategy here!

    machine = psy_machine

    if not machine["DesktopGroupName"]:
        log.warning("🖥 🚧 Machine's 'DesktopGroupName' is empty, skipping: ", machine)
        return

    d_machine, _ = Machine.get_or_new(
        fqdn=machine["DNSName"],
        dg_name=machine["DesktopGroupName"],
        state=machine["SummaryState"],
    )

    # in case none of the machine's attributes changed we use .update() with
    # filtering for the PK to avoid the post-save signal from being triggered
    # exclusively for setting that field (otherwise each call to this function
    # would also trigger that signal):
    if (
        d_machine.state == machine["SummaryState"]
        and d_machine.powerstate == machine["PowerState"]
        and d_machine.maintenance == machine["InMaintenanceMode"]
        and d_machine.registration == machine["RegistrationState"]
        and d_machine.agent == machine["AgentVersion"]
    ):
        Machine.objects.filter(fqdn=machine["DNSName"]).update(updated=True)
        log.debug(f"🖥 ✅ Machine status unchanged: [{d_machine}]")
        return

    d_machine.state = machine["SummaryState"]
    d_machine.powerstate = machine["PowerState"]
    d_machine.maintenance = machine["InMaintenanceMode"]
    d_machine.registration = machine["RegistrationState"]
    d_machine.agent = machine["AgentVersion"]
    d_machine.updated = True
    d_machine.save()
    log.info(f"🖥 ✅ DONE updating details on [{d_machine}]")


def set_maintenance(disable_on, enable_on):
    """Enable or disable maintenance mode for a given machine.

    Parameters
    ----------
    disable_on : list(diop.models.machine.Machine)
        A list (or other iterable) of machine objects for which the maintenance
        mode should be DISABLED.
    enable_on : list(diop.models.machine.Machine)
        A list (or other iterable) of machine objects for which the maintenance
        mode should be ENABLED.

    Notes
    -----
    Maintenance mode on a machine is NOT enforced if the DIOP DB status suggests
    the machine is already in the requested mode! If the DB is outdated this
    will lead to incorrect actions.
    """
    for d_machine in enable_on:
        if d_machine.maintenance:
            log.trace(f"Not changing maintenance, already set to [True]: {d_machine}")
            continue

        if site.in_dry_run_mode(f"ENABLING maintenance mode for: {d_machine}"):
            continue

        log.info(f"ENABLING maintenance mode for: {d_machine}")
        broker.set_maintenance(machine=d_machine.fqdn, disable=False)

    for d_machine in disable_on:
        if not d_machine.maintenance:
            log.trace(f"Not changing maintenance, already set to [False]: {d_machine}")
            continue

        if site.in_dry_run_mode(f"DISABLING maintenance mode for: {d_machine}"):
            continue

        log.info(f"DISABLING maintenance mode for: {d_machine}")
        broker.set_maintenance(machine=d_machine.fqdn, disable=True)


def msg_category_to_psy_style(category: str):
    """Map a message category to a PSyTricks `style` attribute."""
    mapping = {
        "Q": "Question",
        "I": "Information",
        "W": "Exclamation",
        "E": "Critical",
    }
    return mapping[category]


def send_popup(machine: str, subject: str, body: str, category: str):
    """Deliver a pop-up message to a machine.

    Can be passed as a callable to
    `diop.models.notification.Notification.new_popup()` and similar.

    Parameters
    ----------
    machine : str
        The FQDN of the machine to send the message to.
    subject : str
        The message subject / title.
    body : str
        The message body / content.
    category : str
        The MessageTemplate category, will be mapped to a PSyTricks `style`.

    Returns
    -------
    bool
        True in case the pop-up was sent, False otherwise.
    """
    log.debug(f"🖥🎬📢 <send_message> ⏩ [{subject}]@[{machine}]")
    try:
        # FIXME: make dry-run aware!
        broker.send_message(
            machine=machine,
            message=body,
            title=subject,
            style=msg_category_to_psy_style(category),
        )
    except Exception as err:
        log.warning(f"Sending pop-up message failed: {err}")
        return False

    return True


def update_diop_dg_access(dg_name: str):
    """Fetch DG access users via PSyTricks and update the Diop DB accordingly.

    Parameters
    ----------
    dg_name : str
        The name of the delivery group to update.
    """
    dg = DeliveryGroup.objects.get(dg_name=dg_name)

    psy_users = get_dg_access(dg_name=dg_name, strip_domain=True)

    d_users = []
    for psy_user in psy_users:
        try:
            d_users.append(User.objects.get(username=psy_user))
        except:  # ruff: noqa: E722 (bare-except)
            log.info(f"Can't find user [{psy_user}], skipping!")

    dg.access_users.set(d_users)


def get_dg_access(dg_name: str, strip_domain: bool = False) -> list:
    r"""Get unique usernames having access to the given delivery group.

    Parameters
    ----------
    dg_name : str
        The name of the delivery group.
    strip_domain : bool, optional
        If set to `True` the returned list will contain "account names" only,
        meaning the `DOMAINNAME\\` prefix will be stripped.

    Returns
    -------
    list
    """
    usernames = []
    current = broker.get_access_users(dg_name)

    if not current:
        return []

    for user in current:
        name = str(user["Name"])
        if strip_domain:
            try:
                name = name.split("\\")[1]
            except:  # ruff: noqa
                pass
        if name not in usernames:
            usernames.append(name)

    usernames.sort()

    return usernames


def set_dg_access(dg_name: str, usernames: list, keep_common: bool = False):
    """Set access to a DG to be exactly the given list of usernames.

    Check the users currently having access to the given delivery group and add
    / remove permissions so exactly the ones provided in the usernames list are
    permitted to have access (see the `keep_common` parameter description for
    the only exception).

    If the `DIOP_DRY_RUN` setting is active no actual changes to the DG access
    permissions will be issued!

    Parameters
    ----------
    dg_name : str
        The name of the delivery group.
    usernames : list
        The list of usernames that should be permitted to access the DG.
    keep_common : bool, optional
        If set to `True` the user (or group, for that matter) defined in the
        `DIOP_USER_AD_GROUP` setting will be added to the list of accounts that
        are allowed to access the DG. Mostly useful for testing.
    """
    dom_pfx = settings.DIOP_NTDOMAIN
    current = set(get_dg_access(dg_name))
    desired = set()
    for username in usernames:
        if username.startswith(dom_pfx):
            desired.add(username)
            continue
        desired.add(f"{dom_pfx}\\{username}")

    if keep_common:
        desired.add(f"{dom_pfx}\\{settings.DIOP_USER_AD_GROUP.lower()}")
        desired = set(desired)

    if desired == current:
        log.debug("Not changing DG access, given list matches current permissions.")
        return

    to_remove = current.difference(desired)

    log.info(f"Current accounts enabled for DG [{dg_name}]: {current}")
    log.info(f"Accounts to be enabled for DG [{dg_name}]: {desired}")
    log.info(f"Accounts to be DISABLED for DG [{dg_name}]: {to_remove}")

    if site.in_dry_run_mode("adjusting of DG access permissions"):
        return

    broker.set_access_users(group=dg_name, users=",".join(desired), disable=False)
    if to_remove:
        broker.set_access_users(group=dg_name, users=",".join(to_remove), disable=True)

    log.success(
        "Accounts now allowed for DG "
        f"[{dg_name}]: {get_dg_access(dg_name, strip_domain=True)}"
    )


def terminate_session(d_session: Session = None, psy_session_uid: int = None):
    """Request a Diop session to be terminated (machine will be rebooted).

    One of the two optional parameters [d_session, psy_session_uid] is REQUIRED
    to identify the session to be terminated - if both are None a RuntimeError
    will be raised.

    Parameters
    ----------
    d_session : Session, optional
        A Diop session object whose machine should be requested to restart.
    psy_session_uid : int, optional
        A Citrix session UID whose machine should be requested to restart.

    Returns
    -------
    dict
        The parsed `JSON` response of the request's response as delivered by the
        ResTricksWrapper.

    Raises
    ------
    RuntimeError
        Raised in case both optional parameters are None or in case a session
        with the given UID can't be found in the database.
    """
    if not d_session and not psy_session_uid:
        raise RuntimeError("One of [d_session, psy_session_uid] is required!")

    uid = psy_session_uid

    if not d_session:
        # raises a diop.models.session.Session.DoesNotExist if not existing:
        d_session = Session.objects.get(pk=uid)
        log.debug(f"Session [{uid}] is hosted on machine [{d_session.machine}].")

    res = restart_machine(machine=d_session.machine.fqdn)
    record = SiteLog(
        name="Restart requested",
        session=d_session,
        machine=d_session.machine,
        user=d_session.user,
        deliverygroup=d_session.machine.deliverygroup,
        details=res,
    )
    record.save()

    return res


def restart_machine(machine: str):
    """Request a restart (reboot) of the given machine.

    Parameters
    ----------
    machine : str
        The FQDN of the machine to be restarted.

    Returns
    -------
    dict
        The parsed `JSON` response of the request's response as delivered by the
        ResTricksWrapper.
    """
    # FIXME: make dry-run aware!
    return broker.perform_poweraction(machine=machine, action="restart")
