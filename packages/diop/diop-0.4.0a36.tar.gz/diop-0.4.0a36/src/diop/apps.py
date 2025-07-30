from django.apps import AppConfig


class DiopConfig(AppConfig):
    name = "diop"
    verbose_name = "DIOP"

    def ready(self):
        # implicitly connect signal handlers decorated with @receiver.
        from . import signals  # ruff: noqa: F401 (imported but unused)
