from django.apps import AppConfig


class CreateInitialSuperuserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "create_initial_superuser"
    verbose_name = "Create Initial Superuser"
