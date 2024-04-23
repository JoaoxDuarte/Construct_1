from django.apps import AppConfig
from django.core.signals import request_finished


class UsuariosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usuarios'
    
    def ready(self):
        from . import signals
       