from django.apps import AppConfig
from django.core.management import call_command

class DumblympicsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dumblympics_app'

    def ready(self):
        call_command(
            'migrate',
            verbosity=1,
            interactive=False,
            database='default'
        )
