from django.apps import AppConfig
import prodzm

class ProdzmConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prodzm'

    def ready(self):
        import prodzm.signals
