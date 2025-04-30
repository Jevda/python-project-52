# statuses/urls.py
# Файл URL-маршрутизации для приложения statuses

from django.urls import path

# Импортируем все нужные представления из views.py этого приложения
from . import views

app_name = "statuses"

urlpatterns = [
    # Список статусов (/statuses/)
    path("", views.StatusesIndexView.as_view(), name="index"),
    # Создание статуса (/statuses/create/)
    path("create/", views.StatusCreateView.as_view(), name="create"),
    # Редактирование статуса (/statuses/<int:pk>/update/)
    path("<int:pk>/update/", views.StatusUpdateView.as_view(), name="update"),
    # Удаление статуса (/statuses/<int:pk>/delete/)
    path(
        "<int:pk>/delete/",
        views.StatusDeleteView.as_view(),
        name="delete",
    )  # <-- Добавили эту строку
]
