# task_manager/urls.py
# Основной файл URL-маршрутизации проекта task_manager

from django.contrib import admin
from django.urls import path, include
from task_manager import views
# Исправляем импорт views из users
from users import views as views_users # <-- ИЗМЕНЕНО (без task_manager.)

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Исправляем include
    path('users/', include('users.urls')), # <-- ИЗМЕНЕНО (без task_manager.)
    # Вход
    path('login/', views_users.UserLoginView.as_view(), name='login'),
    # Выход
    path('logout/', views_users.UserLogoutView.as_view(), name='logout'),
    # Админка Django
    path('admin/', admin.site.urls),
]