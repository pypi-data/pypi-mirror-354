"""Create Diop default groups and permissions."""

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """Command to create default groups and set up their permissions."""

    help = "Create Diop default groups and set up their permissions"

    @staticmethod
    def setup_group_admins():
        """Set up group `Admins`.

        The group will simply have **all** permissions assigned.
        """
        print("Adding auth group 'Admins'...")
        group, created = Group.objects.get_or_create(name="Admins")
        for newperm in Permission.objects.all():
            print(f"Adding permission [{newperm}]...")
            group.permissions.add(newperm)

    @staticmethod
    def setup_group(name, natural_keys):
        """Set up a group and assign permissions as defined.

        Parameters
        ----------
        name : str
            The name of the group. Note: the group may already exist, in which
            case only the permissions will be set accordingly.
        natural_keys : list
            A list of 3-tuples (`app_label`, `model`, `codename`) to be used as
            parameters for the `Permission.objects.get_by_natural_key()` call.
            The permissions defined in this list will be assigned to the group,
            any permission not present in the list will be removed!
        """
        new_permissions = []
        print(f"Adding auth group '{name}'...")
        group, created = Group.objects.get_or_create(name=name)
        for natural_key in natural_keys:
            newperm = Permission.objects.get_by_natural_key(
                app_label=natural_key[1],
                model=natural_key[2],
                codename=natural_key[0],
            )
            print(f"Adding permission [{newperm}]...")
            group.permissions.add(newperm)
            new_permissions.append(newperm)

        for permission in group.permissions.all():
            if permission not in new_permissions:
                print(f"Removing unexpected 🦹 permission [{permission}]...")
                group.permissions.remove(permission)

    def handle(self, *args, **options):
        """Perform group creation and permission assignment.

        Note
        ----
        To figure out how a specific 3-tuple is called, the following code may
        be used in a `shell_plus` session:

        ```Python
        for perm in Permission.objects.all():
            if "template" in perm.natural_key()[0]:
                print(perm.natural_key())
        ```
        """
        Command.setup_group_admins()

        operators_permissions = [
            # "view" permissions:
            ("view_logentry", "admin", "logentry"),
            ("view_group", "auth", "group"),
            ("view_permission", "auth", "permission"),
            ("view_user", "auth", "user"),
            ("view_contenttype", "contenttypes", "contenttype"),
            ("view_deliverygroup", "diop", "deliverygroup"),
            ("view_issue", "diop", "issue"),
            ("view_machine", "diop", "machine"),
            ("view_messagetemplate", "diop", "messagetemplate"),
            ("view_notification", "diop", "notification"),
            ("view_ppmsbooking", "diop", "ppmsbooking"),
            ("view_reservation", "diop", "reservation"),
            ("view_session", "diop", "session"),
            ("view_sessionproperties", "diop", "sessionproperties"),
            ("view_sitelog", "diop", "sitelog"),
            ("view_task", "diop", "task"),
            ("view_user", "diop", "user"),
            ("view_failure", "django_q", "failure"),
            ("view_ormq", "django_q", "ormq"),
            ("view_schedule", "django_q", "schedule"),
            ("view_success", "django_q", "success"),
            ("view_task", "django_q", "task"),
            ("view_session", "sessions", "session"),
            ("view_site", "sites", "site"),
            # "add" permissions:
            ### ("add_task", "diop", "task"),  # do NOT assign!
            ("add_task", "django_q", "task"),
            ("add_messagetemplate", "diop", "messagetemplate"),
            # "change" permissions:
            ("change_messagetemplate", "diop", "messagetemplate"),
            # "delete" permissions:
            ("delete_messagetemplate", "diop", "messagetemplate"),
            ("delete_failure", "django_q", "failure"),  # delete Failed task
            ("delete_ormq", "django_q", "ormq"),  # delete Queued task
        ]
        Command.setup_group(name="Operators", natural_keys=operators_permissions)

        users_permissions = [
            ("view_contenttype", "contenttypes", "contenttype"),
            ("view_session", "sessions", "session"),
            ("view_deliverygroup", "diop", "deliverygroup"),
            ("view_machine", "diop", "machine"),
            ("view_session", "diop", "session"),
            ("view_sessionproperties", "diop", "sessionproperties"),
        ]
        Command.setup_group(name="Users", natural_keys=users_permissions)
