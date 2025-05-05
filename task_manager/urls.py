from django.contrib import admin
from django.urls import include, path
from django.utils import translation

from task_manager import views
from users import views as views_users

# Активируем русский язык при загрузке urls.py
translation.activate('ru')

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", include("users.urls")),
    path("statuses/", include("statuses.urls")),
    path("tasks/", include("tasks.urls")),
    path("labels/", include("labels.urls")),
    path("login/", views_users.UserLoginView.as_view(), name="login"),
    path("logout/", views_users.UserLogoutView.as_view(), name="logout"),
    path("admin/", admin.site.urls),
]