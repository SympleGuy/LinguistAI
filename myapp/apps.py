from django.apps import AppConfig

class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'

    def ready(self):
        # Python 3.14 + Django 4.2 test runner Context copy compatibility fix
        try:
            from django.template.context import BaseContext
            def _basecontext_copy(self):
                duplicate = self.__class__.__new__(self.__class__)
                duplicate.dicts = self.dicts[:]
                return duplicate
            BaseContext.__copy__ = _basecontext_copy
        except Exception:
            pass