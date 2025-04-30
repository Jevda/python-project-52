# task_manager/settings.py
# Стандартный файл настроек Django для проекта task_manager.

import os
import dj_database_url
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные окружения из .env файла
load_dotenv()
# Определяем базовую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent
# Получаем секретный ключ из переменных окружения
SECRET_KEY = os.getenv('SECRET_KEY')
# Определяем режим DEBUG (True, если DJANGO_DEBUG не 'False')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') != 'False'

# Список разрешенных хостов
ALLOWED_HOSTS = [
    'webserver',  # Для docker-compose
    '127.0.0.1',
    'localhost',
    'python-project-52-tvt9.onrender.com' # Убедись, что здесь твой актуальный URL Render
]

# Application definition
INSTALLED_APPS = [
    # Стандартные приложения Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    # Whitenoise для статики
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',

    # Сторонние приложения
    'django_bootstrap5', # Для интеграции с Bootstrap 5
    'django_filters',    # Для фильтрации (понадобится позже)

    # Наши приложения
    'users', # <-- ИЗМЕНЕНО ЗДЕСЬ (было 'users.apps.UsersConfig')
    'statuses', # Указываем только имя приложения
    'tasks',    # Указываем только имя приложения
    # 'labels',     # Добавим позже, когда будет приложение labels
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Whitenoise middleware (рекомендуется размещать после SecurityMiddleware)
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной файл URL-конфигурации
ROOT_URLCONF = 'task_manager.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Указываем Django искать шаблоны в папке 'templates' в корне проекта
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True, # Разрешаем Django искать шаблоны внутри папок 'templates' приложений
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

# Конфигурация WSGI
WSGI_APPLICATION = 'task_manager.wsgi.application'


# Database
# Используем dj_database_url для настройки БД из переменной окружения DATABASE_URL
# По умолчанию используется SQLite для локальной разработки
DATABASES = {
    'default': dj_database_url.config(
        # Если DATABASE_URL не задана, используем sqlite
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        # Время жизни соединения с БД (для PostgreSQL)
        conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


# Internationalization
LANGUAGE_CODE = 'ru-RU' # Устанавливаем русский язык
TIME_ZONE = 'Europe/Riga' # Устанавливаем временную зону
USE_I18N = True # Включаем интернационализацию (для переводов)
USE_TZ = True # Включаем поддержку временных зон


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/' # URL для статических файлов
# Директория, куда будут собираться все статические файлы командой collectstatic
STATIC_ROOT = BASE_DIR / 'staticfiles'
# Хранилище для статики, оптимизированное Whitenoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки перенаправления после входа/выхода и URL страницы входа
LOGIN_REDIRECT_URL = '/' # Куда перенаправлять после успешного входа
LOGOUT_REDIRECT_URL = '/' # Куда перенаправлять после выхода
LOGIN_URL = 'login' # Имя URL-маршрута для страницы входа
