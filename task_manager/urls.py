# task_manager/urls.py
# Основной файл URL-маршрутизации проекта task_manager

from django.contrib import admin
from django.urls import path
# Импортируем наше созданное представление 'index' из views.py
from task_manager import views

urlpatterns = [
    # Маршрут для админки Django (мы пока ее не используем, но оставим)
    path('admin/', admin.site.urls),
    # Маршрут для главной страницы ('')
    # Он будет вызывать функцию 'index' из нашего файла views.py
    # name='index' - это имя маршрута, полезно для ссылок в шаблонах
    path('', views.index, name='index'),
]
