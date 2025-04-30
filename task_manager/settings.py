# task_manager/settings.py
# Стандартный файл настроек Django для проекта task_manager.
import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') != 'False'

ALLOWED_HOSTS = [
    'webserver',
    '127.0.0.1',
    'localhost',
    'python-project-52-tvt9.onrender.com' # Убедись, что здесь твой актуальный URL
]

# Application definition
INSTALLED_APPS = [
    # Стандартные приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Whitenoise
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # Сторонние приложения
    'django_bootstrap5',
    'django_filters',
    # Наши приложения
    'users.apps.UsersConfig',
    'statuses.apps.StatusesConfig',
    'tasks.apps.TasksConfig',
    'labels.apps.LabelsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'task_manager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'task_manager.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
}

# --- ИЗМЕНЕНИЯ ЗДЕСЬ ---
# Определяем валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        # Используем только валидатор минимальной длины
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        # Устанавливаем минимальную длину в 3 символа
        'OPTIONS': {
            'min_length': 3,
        }
    },
    # Убрали остальные стандартные валидаторы:
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]
# --- КОНЕЦ ИЗМЕНЕНИЙ ---

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Riga'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'
