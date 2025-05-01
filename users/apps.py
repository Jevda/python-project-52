# users/apps.py
# Файл конфигурации приложения users

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    # Указываем имя приложения (без task_manager.)
    name = "users" # <-- ИЗМЕНЕНО
