"""Management command `pdoc`.

This is required as calling `pdoc` normally results in an error message saying
`Error importing 'module': AppRegistryNotReady: Apps aren't loaded yet.` or
similar.

Example
-------

```bash
SETTINGS_ENV=diop.env diop-manage \
    pdoc \
    -o build/docs \
    -d numpy \
    diop \
    diop_core \
    !diop.migrations \
    !diop.management
```
"""

from pathlib import Path
from django.core.management.base import BaseCommand
from pdoc.__main__ import cli, parser


class Command(BaseCommand):
    """Command class for the `pdoc` management command."""

    def run_from_argv(self, argv: list[str]) -> None:
        """Entry point for `diop-manage`.

        Parameters
        ----------
        argv : list[str]
            The command line argument vector that is passed on by `diop-manage`
            (or `django-admin` for that matter).
        """
        parser.prog = " ".join((Path(argv[0]).name, argv[1]))
        cli(argv[2:])
