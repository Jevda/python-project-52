# task_manager/urls.py
# Основной файл URL-маршрутизации проекта task_manager

from django.contrib import admin
from django.urls import path, include
# Импортируем views из основного приложения task_manager
from task_manager import views
# Импортируем views из приложения users под псевдонимом views_users
from users import views as views_users

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Приложение Users (без login/logout)
    path('users/', include('users.urls')),
    # Приложение Statuses
    path('statuses/', include('statuses.urls')),
    # Приложение Tasks
    path('tasks/', include('tasks.urls')),  # Добавляем маршруты для задач
    # Login и Logout
    path('login/', views_users.UserLoginView.as_view(), name='login'),
    path('logout/', views_users.UserLogoutView.as_view(), name='logout'),
    # Админка Django
    path('admin/', admin.site.urls),
]
