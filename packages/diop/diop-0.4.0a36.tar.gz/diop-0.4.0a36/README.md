# Diop 🕶

- `D`esktop
- `I`nfrastructure
- `Op`erations

`Diop` is a [Django-based][www-django] web application to manage a Virtual
Desktop Infrastructure based on *Citrix Virtual Apps and Desktops* (CVAD).

## 🧩 Components and ⚙ functional dependencies

A full Diop setup consists of the following components:

- The Diop main project components:
  - The Diop **core app**.
  - Several Diop [Django-Q2][www-django-q2] **task queue workers**. They are
    performing the periodic tasks, updating status information and similar.
- A backing database, currently only **MySQL** is tested.
- Optional, but **required for production** setups:
  - Access to a running [**PSyTricks / ResTricks**][www-psytricks] service  -
    that's the interface to the *CVAD* platform (in a testing / development
    setup this is not necessarily required, but then obviously no status updates
    and / or actions can be performed).
- Optional, but **highly recommended**:
  - Access to an **ActiveDirectory LDAP** interface for performing
    authentication.
  - Access to a **PPMS booking system** instance (performed through the
    [pyppms][www-pyppms] package).

[www-django]: https://www.djangoproject.com/
[www-psytricks]: https://pypi.org/project/psytricks/
[www-pyppms]: https://pypi.org/project/pyppms/
[www-django-q2]: https://github.com/django-q2/django-q2
