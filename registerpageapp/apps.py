from django.apps import AppConfig


class RegisterpageappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'registerpageapp'

    def ready(self):
        import registerpageapp.signals  # noqa: F401
