# statuses/tests.py
# Файл для тестов приложения statuses

import http

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusViewsTests(TestCase):

    def setUp(self):
        """Создаем пользователя, статус и логинимся."""
        self.user_data = {
            "username": "testuser_status",
            "password": "Password123!",
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        self.status_data = {"name": "Initial Status"}
        self.status = Status.objects.create(**self.status_data)
        # Сохраняем все нужные URL'ы
        self.statuses_index_url = reverse("statuses:index")
        self.status_create_url = reverse("statuses:create")
        # E501 fix
        self.status_update_url = reverse(
            "statuses:update", args=[self.status.pk],
        )
        # URL удаления
        # E501 fix
        self.status_delete_url = reverse(
            "statuses:delete", args=[self.status.pk],
        )
        self.login_url = reverse("login")

    def test_status_list_view_requires_login(self):
        """Проверяет, что список статусов требует логина."""
        self.client.logout()
        response = self.client.get(self.statuses_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(response.url.split("?")[0], self.login_url)

    def test_status_list_view_get_success(self):
        # E501 fix
        """Проверяет доступность и шаблон списка статусов
        для залогиненного пользователя."""
        response = self.client.get(self.statuses_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "statuses/index.html")
        self.assertContains(response, self.status_data["name"])

    def test_status_create_view_get(self):
        """Проверяет доступность и шаблон страницы создания статуса."""
        response = self.client.get(self.status_create_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "statuses/create.html")

    def test_status_create_view_post_success(self):
        """Проверяет создание статуса и редирект."""
        new_status_data = {"name": "New Test Status"}
        # E501 fix
        response = self.client.post(
            self.status_create_url, data=new_status_data,
        )
        self.assertTrue(Status.objects.filter(name=new_status_data["name"]).exists())
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.statuses_index_url)

    def test_status_update_view_get_success(self):
        """Проверяет доступность и шаблон страницы редактирования статуса."""
        response = self.client.get(self.status_update_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "statuses/update.html")
        self.assertContains(response, self.status_data["name"])

    def test_status_update_view_post_success(self):
        """Проверяет успешное обновление статуса."""
        updated_data = {"name": "Updated Status Name"}
        response = self.client.post(self.status_update_url, data=updated_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.statuses_index_url)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, updated_data["name"])

    def test_status_delete_view_get_success(self):
        """Проверяет доступ к странице подтверждения удаления статуса."""
        response = self.client.get(self.status_delete_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "statuses/delete.html")
        self.assertContains(response, self.status_data["name"])

    # --- Финальный тест для статусов ---
    def test_status_delete_view_post_success(self):
        """Проверяет успешное удаление статуса (POST).
        """
        status_pk_to_delete = self.status.pk
        initial_status_count = Status.objects.count()
        response = self.client.post(self.status_delete_url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.statuses_index_url)

        # E501 fix
        status_exists_after_delete = Status.objects.filter(
            pk=status_pk_to_delete
        ).exists()
        # E501 fix
        self.assertFalse(
            status_exists_after_delete, "Статус не был удален из БД",
        )
        # E501 fix
        self.assertEqual(
            Status.objects.count(), initial_status_count - 1,
            "Количество статусов не уменьшилось",
        )
