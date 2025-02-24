from django.apps import AppConfig


class PlanetariumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "planetarium"

    def ready(self):
        import planetarium.signals