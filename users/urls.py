# users/urls.py
"""URL configuration for the users application."""

from django.urls import path

# Импортируем все нужные представления из views.py этого приложения
from . import views

app_name = "users"

urlpatterns = [
    # Список пользователей (/users/)
    path("", views.UsersIndexView.as_view(), name="index"),
    # Регистрация (/users/create/)
    path("create/", views.UserRegisterView.as_view(), name="create"),
    # Редактирование (/users/<int:pk>/update/)
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="update"),
    # Удаление (/users/<int:pk>/delete/)
    # Комментарий перенесен для E501
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="delete"),
]