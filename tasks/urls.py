# tasks/urls.py
from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TasksIndexView.as_view(), name="index"),
    path("create/", views.TaskCreateView.as_view(), name="create"),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="delete"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="detail"),
]
