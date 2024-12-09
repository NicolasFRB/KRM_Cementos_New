from django.apps import AppConfig
from health_check.plugins import plugin_dir

class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'krm.base'

    def ready(self):
            from healthchecks import KrmToolSimpleCheck
            plugin_dir.register(KrmToolSimpleCheck)
