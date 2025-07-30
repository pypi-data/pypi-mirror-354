"""Create Diop systemd service unit files."""

from pathlib import Path
from textwrap import dedent
import sys

from django.core.management.base import BaseCommand, CommandError

from diop_core.settings import env


_SETTINGS_ENV = Path(env.str("SETTINGS_ENV")).resolve()
_VENV_BIN = Path(sys.executable).parent
# NOTE: Path(env.str("VIRTUAL_ENV")) fails when venv not activated


class Command(BaseCommand):
    """Command to create systemd service unit files."""

    help = "Create Diop systemd service unit files"

    @staticmethod
    def q2_unit(desc, cluster, workingdir=None, loglevel="SUCCESS"):
        """Render a systemd unit file content for a Django-Q2 worker.

        Parameters
        ----------
        desc : str
            The description to put into the `Unit.Description` field. Will be
            prefixed with `Diop Task Queue - `.
        cluster : str
            The name of the cluster that the worker started by this unit file
            will belong to (used for the `Q_CLUSTER_NAME` environment variable).
        workingdir : str, optional
            The value to set for `Service.WorkingDirectory`, by default
            `/home/django`.
        loglevel : str, optional
            The loguru loglevel name, by default `SUCCESS`.

        Returns
        -------
        str
        """
        workingdir = workingdir if workingdir else "/home/django"

        content = f"""
        [Unit]
        Description=Diop Task Queue - {desc}
        After=network.target

        [Service]
        User=django
        WorkingDirectory={workingdir}
        Environment=SETTINGS_ENV={_SETTINGS_ENV}
        Environment=LOGURU_LEVEL={loglevel}
        Environment=Q_CLUSTER_NAME={cluster}
        ExecStartPre={_VENV_BIN}/diop-manage migrate
        ExecStart={_VENV_BIN}/diop-manage qcluster

        [Install]
        WantedBy=multi-user.target
        """
        return dedent(content[1:])

    @staticmethod
    def diop_web_unit(workers=2, bind=None, workingdir=None, loglevel="SUCCESS"):
        """Render the systemd unit file content for the Diop gunicorn service.

        Parameters
        ----------
        workers : int, optional
            Number of gunicorn workers, by default 2
        bind : str, optional
            The bind address and port for gunicorn, will use `0.0.0.0:8000` in
            case it's not specified.
        workingdir : str, optional
            The value to set for `Service.WorkingDirectory`, by default
            `/home/django`.
        loglevel : str, optional
            The loguru loglevel name, by default `SUCCESS`.

        Returns
        -------
        str
        """
        workingdir = workingdir if workingdir else "/home/django"
        bind = bind if bind else "0.0.0.0:8000"

        content = f"""
        [Unit]
        Description=Diop Gunicorn web service
        After=network.target

        [Service]
        User=django
        WorkingDirectory={workingdir}
        Environment=SETTINGS_ENV={_SETTINGS_ENV}
        Environment=LOGURU_LEVEL={loglevel}
        ExecStartPre={_VENV_BIN}/diop-manage migrate
        ExecStart={_VENV_BIN}/gunicorn --workers {workers} --bind {bind} diop_core.wsgi

        [Install]
        WantedBy=multi-user.target
        """
        return dedent(content[1:])

    @staticmethod
    def write_units(outdir):
        """Write all unit files into the given directory.

        The target directory will be created in case it's not present, existing
        unit files will NOT be overwritten!

        Parameters
        ----------
        outdir : str or Path
            Where to create the unit files.
        """

        def write_file(fpath: Path, content: str):
            if fpath.exists():
                print(f"ERROR: file [{fpath}] already exists, skipping!")
                return
            fpath.write_text(content)
            print(fpath)

        outdir = Path(outdir).resolve()
        outdir.mkdir(exist_ok=True)

        print("Writing systemd unit files:")
        unitfile = outdir / "diop-web.service"
        write_file(unitfile, Command.diop_web_unit())

        q2_units = [
            ("activedirectory", "ActiveDirectory Tasks (5m)"),
            ("housekeeping", "Housekeeping Tasks (15m)"),
            ("ppms-long", "PPMS tasks LONG (15m)"),
            ("ppms-short", "PPMS tasks SHORT (30s)"),
            ("statusupdates", "Status Update Tasks"),
        ]
        for unit in q2_units:
            cluster = unit[0]
            desc = unit[1]
            unitfile = outdir / f"diop-q2-{cluster}.service"
            write_file(unitfile, Command.q2_unit(desc, cluster))

    def add_arguments(self, parser):
        """Add commandline arguments to the parser."""
        parser.add_argument(
            "--outdir",
            type=str,
            required=True,
            help="Directory where to store the unit files.",
        )

    def handle(self, *args, **options):
        """Entry point method for the management command."""
        Command.write_units(options["outdir"])
