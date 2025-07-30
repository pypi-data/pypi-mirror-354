"""Wrapper replacing Django's default `manage.py` file.

Examples
--------
Run the Diop application using the built-in server (development only).
```bash
SETTINGS_ENV=diop-dev.env diop-manage runserver
```

Run the [`shell_plus` Django extension][shellplus]:
```bash
SETTINGS_ENV=diop-dev.env diop-manage shell_plus
```

[shellplus]: https://django-extensions.readthedocs.io/en/latest/shell_plus.html
"""

import os
import sys

from random import choices
from string import ascii_letters, digits
from textwrap import dedent


def manage():
    """Entry-point for running administrative tasks (replaces `manage.py`)."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "diop_core.settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


def newconfig():
    """Print a config file template, pre-filled with some reasonable values."""
    secret = "".join(choices(ascii_letters + digits, k=64))
    config = f"""
    # Django secret key, used for session data, cookies and temporary tokens.
    # Changing the key will invalidate those, but won't affect user passwords.
    SECRET_KEY={secret}

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG=False

    ALLOWED_HOSTS=127.0.0.1,localhost,diop.vdi.example.xy,diop-core.lxd

    DATABASE_URL=mysql://diop:diop_db_password@diop-db.lxd:3306/diop

    AUTH_LDAP_SERVER_URI=ldaps://dc.domainname.ads.example.xy
    AUTH_LDAP_BIND_DN=ldapbinduser@domainname.ads.example.xy
    AUTH_LDAP_BIND_PASSWORD=LdApBiNdPaSsWoRd
    AUTH_LDAP_BASE_DN=DC=domainname,DC=ads,DC=example,DC=xy

    EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
    EMAIL_HOST=not.relevant.for.console.backend

    PYPPMS_API_KEY=WhatAWonderfulKey
    PYPPMS_URI=https://ppms.eu/example/pumapi/
    PYPPMS_CACHE=/tmp/pyppms_cache/
    PYPPMS_CORE_REF=2
    PYPPMS_LOC_FILTER=vdi.example.xy
    PYPPMS_NAME_GROUPS=Argon,Helium,Neon


    # ResTricks server address:
    PSYTRICKS_BASE_URL="http://localhost:8080/"
    # Verify ResTricks server version when connecting:
    PSYTRICKS_VERIFY=True


    DIOP_USER_AD_GROUP=EXMPL-VDI-Users
    DIOP_SUPPORT_CONTACT=vdi-support@example.xy
    DIOP_DISCONNECTED_MAX=75
    DIOP_NTDOMAIN=EXAMPLE

    # Switching on "graceful" mode will make several tasks run in a less impacting
    # way, e.g. removing access to a DG will be done such that the standard group
    # will still be allowed to connect. Most likely not useful in production!
    DIOP_GRACEFUL=True

    # Switching on "dry-run" mode will prevent certain actions from doing effective
    # changes to the platform, i.e. changing access permissions or terminating
    # sessions. It will NOT affect components fetching status information to update
    # the DB, or strictly informational effects like e-mails or pop-up messages
    # (they will run normally). Actions that will be skipped due to dry-run being
    # active will print a warning-level message to the log instead.
    DIOP_DRY_RUN=False"""
    print(dedent(config))
