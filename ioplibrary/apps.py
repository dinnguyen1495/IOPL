from django.apps import AppConfig


class IopLibraryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ioplibrary'
    verbose_name = 'IOP\'s Library'

    def ready(self):
        import ioplibrary.signals