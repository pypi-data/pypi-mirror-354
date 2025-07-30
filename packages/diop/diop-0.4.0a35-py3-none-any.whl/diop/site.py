"""Diop site related functions."""

from django.conf import settings
from django.contrib.sites.models import Site

from loguru import logger as log


def name():
    """Get the configured 'Site Name'."""
    return Site.objects.get(pk=settings.SITE_ID).name


def booking_uri():
    """Get the URI of the PPMS web interface for the configured core facility."""
    # FIXME: should rather be in the adapter module (to allow for potentially
    # other booking system adapters) but this currently leads to a circular
    # import - for now the function stays here, reconsider at a later point.
    pumapi = str(settings.PYPPMS_URI)
    cf_ref = settings.PYPPMS_CORE_REF
    return pumapi.replace("pumapi/", f"login/?pf={cf_ref}")


def in_dry_run_mode(msg: str) -> bool:
    """Check if "dry-run" mode is active and log a warning message if yes.

    This is intended as a shorthand to limit the amount of code necessary for
    evaluating if the `DIOP_DRY_RUN` setting is true and issue a warning to the
    log with a situation-specific message.

    Parameters
    ----------
    msg : str
        The caller-specific description to be added to the warning log message.

    Returns
    -------
    bool
    """
    if not settings.DIOP_DRY_RUN:
        return False

    log.warning(f"[🫧DRY-RUN🫧]: {msg} will be skipped...")
    return True
