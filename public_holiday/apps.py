from django.apps import AppConfig


class PublicHolidayConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "public_holiday"

    def ready(self):
        from . import signals  # noqa: F401
