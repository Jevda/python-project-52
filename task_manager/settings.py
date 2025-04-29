# task_manager/settings.py
# Стандартный файл настроек Django для проекта task_manager.

# Импортируем необходимые модули
import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные окружения из файла .env
load_dotenv()

# Определяем базовую директорию проекта
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Получаем секретный ключ из переменных окружения
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Устанавливаем режим DEBUG в зависимости от переменной окружения
# Если DJANGO_DEBUG не 'False', то DEBUG будет True
DEBUG = os.getenv('DJANGO_DEBUG', 'True') != 'False'

# Список разрешенных хостов.
# 'webserver' нужен для тестов Хекслета.
# '127.0.0.1' и 'localhost' - для локальной разработки.
ALLOWED_HOSTS = [
    'webserver',
    '127.0.0.1',
    'localhost',
    'python-project-52-tvt9.onrender.com/',
]


# Application definition

INSTALLED_APPS = [
    # Стандартные приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Добавляем Whitenoise для обслуживания статических файлов в продакшене
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    # Наши приложения (пока пусто, будем добавлять позже)
    # 'task_manager.users',
    # 'task_manager.statuses',
    # 'task_manager.tasks',
    # 'task_manager.labels',
    # Сторонние приложения
    'django_bootstrap5', # Для интеграции с Bootstrap 5
    'django_filters', # Для фильтрации (добавим позже)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Добавляем Whitenoise Middleware СРАЗУ ПОСЛЕ SecurityMiddleware
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
        # Указываем Django искать шаблоны в папке templates в корне проекта
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Настройка базы данных через переменную окружения DATABASE_URL
# Используем dj_database_url для парсинга URL
# Для локальной разработки можно использовать SQLite,
# указав DATABASE_URL=sqlite:///db.sqlite3 в .env файле.
# Для продакшена на Render будет использоваться URL их PostgreSQL базы.
DATABASES = {
    'default': dj_database_url.config(
        # Указываем соединение по умолчанию, если DATABASE_URL не задана
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600 # Время жизни соединения с БД (опционально)
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-RU' # Устанавливаем русский язык по умолчанию

TIME_ZONE = 'Europe/Riga' # Устанавливаем твой часовой пояс

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/' # URL для статических файлов
# Директория, куда collectstatic будет собирать все статические файлы для продакшена
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Включаем сжатие файлов для Whitenoise (уменьшает размер статики)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Дополнительные настройки для Bootstrap5
#BOOTSTRAP5 = {
#    "css_url": {
#        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css",
#        "integrity": "sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH",
#        "crossorigin": "anonymous",
#    },
#    "javascript_url": {
#        "url": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js",
#        "integrity": "sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz",
#        "crossorigin": "anonymous",
#    },
#}

# Настройки для django-filter (пока не используются)
# FILTERS_EMPTY_CHOICE_LABEL = '---------' # Текст для пустого выбора в фильтре