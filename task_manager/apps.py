from django.apps import AppConfig
from django.utils import translation


class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'

    def ready(self):
        # Активируем русский язык при каждом запуске приложения
        translation.activate('ru')
