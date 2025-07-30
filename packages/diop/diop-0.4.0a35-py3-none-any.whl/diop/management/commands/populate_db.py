"""Populate the Diop database with provided fixtures."""

from glob import glob
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.core.management.commands import loaddata


class Command(BaseCommand):
    """Command to load provided fixtures into the Diop database.

    This is a convenience wrapper to facilitate the initial setup and simplify
    the installation commands. All it does is to figure out the path to the
    provided YAML fixtures and call the `handle()` method on the `loaddata`
    management command object with the appropriate parameters.
    """

    help = "Populate the Diop database with provided fixtures"

    def handle(self, *args, **options):
        """Entry point method for the management command."""
        fixt_dir = Path(__file__).parent.parent.parent / "fixtures"
        fixtures = glob(str(fixt_dir / "*.yaml"))

        # the minimal options dict for calling handle() below:
        lf_options = {
            "verbosity": 3,
            "database": "default",
            "app_label": None,
            "ignore": False,
            "exclude": [],
            "format": "yaml",
        }

        loadfixtures = loaddata.Command()
        loadfixtures.handle(*fixtures, **lf_options)
