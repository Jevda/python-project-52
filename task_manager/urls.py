# task_manager/urls.py
"""task_manager URL Configuration."""

from django.contrib import admin
from django.urls import include, path

from task_manager import views
from users import views as views_users

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("tasks/", include("tasks.urls")),
    path("labels/", include("labels.urls")),  # Добавили маршруты для меток
    path("login/", views_users.UserLoginView.as_view(), name="login"),
    path("logout/", views_users.UserLogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
]
