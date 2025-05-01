# task_manager/settings.py
import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")
# Рекомендуется использовать 'False' в продакшене, но 'True' удобно для разработки и тестов
DEBUG = os.getenv("DJANGO_DEBUG", "True") != "False"

ALLOWED_HOSTS = [
    "webserver", # Для Docker Compose в тестах GitHub Actions/Hexlet
    "127.0.0.1",
    "localhost",
    # Замените на ваш реальный домен на Render
    "python-project-52-tvt9.onrender.com",
]

# Список установленных приложений
INSTALLED_APPS = [
    # Стандартные приложения Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    # Whitenoise для статики (должен быть перед staticfiles, если используется runserver_nostatic)
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    # Сторонние приложения
    "django_bootstrap5", # Для интеграции с Bootstrap 5
    "django_filters",    # Для фильтрации
    # Наши приложения - указываем через AppConfig
    "users.apps.UsersConfig",
    "statuses.apps.StatusesConfig",
    "tasks.apps.TasksConfig",
    "labels.apps.LabelsConfig",
]

# Промежуточное ПО (Middleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Whitenoise Middleware (рекомендуется размещать после SecurityMiddleware)
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Основной файл URL-конфигурации
ROOT_URLCONF = "task_manager.urls"

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Указываем Django искать шаблоны в папке templates в корне проекта
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True, # Разрешаем Django искать шаблоны внутри папок приложений (templates/)
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# WSGI приложение для развертывания
WSGI_APPLICATION = "task_manager.wsgi.application"

# Настройки базы данных
DATABASES = {
    "default": dj_database_url.config(
        # По умолчанию используем SQLite для локальной разработки
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        # DATABASE_URL будет взят из .env или переменных окружения для PostgreSQL
        conn_max_age=600, # Время жизни соединения с БД (для PostgreSQL)
    ),
}

# Настройки валидации паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        # Оставляем только валидатор минимальной длины
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 3, # Устанавливаем минимальную длину 3
        },
    },
]

# Настройки интернационализации
LANGUAGE_CODE = "ru-RU" # Язык по умолчанию
TIME_ZONE = "Europe/Riga" # Ваша временная зона
USE_I18N = True # Включаем систему переводов
USE_TZ = True # Включаем поддержку временных зон

# Настройки статических файлов
STATIC_URL = "static/" # URL для статических файлов
STATIC_ROOT = BASE_DIR / "staticfiles" # Папка для сбора статики командой collectstatic
# Настройка хранилища для Whitenoise (оптимизация статики)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Тип автоинкрементного поля для первичных ключей
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URL'ы для перенаправления после входа/выхода и URL страницы входа
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
LOGIN_URL = "login" # Имя URL-маршрута для страницы входа

# Опционально: Настройки Rollbar (добавятся на этапе 8)
# ROLLBAR = {
#     'access_token': os.getenv('ROLLBAR_ACCESS_TOKEN'),
#     'environment': 'development' if DEBUG else 'production',
#     'code_version': '1.0',
#     'root': BASE_DIR,
# }
# import rollbar
# rollbar.init(**ROLLBAR)
