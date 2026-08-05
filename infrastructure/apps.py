from django.apps import AppConfig


class InfrastructureConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "infrastructure"

    def ready(self):
        # Importing the module is what connects the signal receivers.
        from infrastructure import signals  # noqa: F401
