from django.apps import AppConfig


class ControlUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'control_user'
    def ready(self) :
        import control_user.signals
