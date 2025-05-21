from django.apps import AppConfig


class B111Config(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'b11_1'

    def ready(self):
        import b11_1.utils.signals  # Ensure signals are imported
