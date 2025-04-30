# users/apps.py
"""App configuration for the users application."""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configuration class for the 'users' Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    # Указываем имя приложения (без task_manager.)
    name = "users" # <-- ИЗМЕНЕНО