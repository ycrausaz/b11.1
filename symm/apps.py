from django.apps import AppConfig


class B111Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'symm'

    def ready(self):
        import symm.signals  # Ensure signals are imported
