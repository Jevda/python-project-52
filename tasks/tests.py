# tasks/tests.py
# Файл для тестов приложения tasks

import http  # Модуль со стандартными кодами HTTP-статусов

from django.contrib.auth.models import User  # Стандартная модель пользователя
from django.test import TestCase  # Базовый класс для тестов Django
from django.urls import reverse  # Функция для получения URL по имени

# !!! Добавляем импорт модели Label !!!
from labels.models import Label
from statuses.models import Status

# Импортируем модели, необходимые для тестов
from .models import Task


# Класс для тестов представлений (views) задач
class TaskViewsTests(TestCase):

    def setUp(self):
        """Создаем тестовые данные перед каждым тестом."""
        # Создаем пользователей
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123!",
        }
        self.user = User.objects.create_user(**self.user_data)

        self.other_user_data = {
            "username": "otheruser",
            "first_name": "Other",
            "last_name": "User",
            "password": "OtherPassword456!",
        }
        self.other_user = User.objects.create_user(**self.other_user_data)

        # Создаем статус
        self.status = Status.objects.create(name="Test Status")

        # Создаем задачу
        self.task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": self.status,
            "author": self.user,
            "executor": self.other_user,
        }
        self.task = Task.objects.create(**self.task_data)

        # Логиним основного пользователя
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )

        # Сохраняем URL'ы для удобства
        self.tasks_index_url = reverse("tasks:index")
        self.task_create_url = reverse("tasks:create")
        self.task_detail_url = reverse("tasks:detail", args=[self.task.pk])
        self.task_update_url = reverse("tasks:update", args=[self.task.pk])
        self.task_delete_url = reverse("tasks:delete", args=[self.task.pk])
        self.login_url = reverse("login")

    # --- Существующие тесты CRUD ---
    def test_tasks_list_view_requires_login(self):
        """Проверяет, что список задач требует логина."""
        self.client.logout()
        response = self.client.get(self.tasks_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(response.url.split("?")[0], self.login_url)

    def test_tasks_list_view_success(self):
        """Проверяет доступность и шаблон списка задач."""
        response = self.client.get(self.tasks_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertContains(response, self.task_data["name"])

    def test_task_create_view_get(self):
        """Проверяет доступность и шаблон страницы создания задачи."""
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/create.html")

    def test_task_create_view_post_success(self):
        """Проверяет создание задачи и редирект."""
        new_task_data = {
            "name": "New Test Task",
            "description": "New Test Description",
            "status": self.status.pk,
            "executor": self.other_user.pk,
        }
        response = self.client.post(self.task_create_url, data=new_task_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)
        self.assertTrue(Task.objects.filter(name=new_task_data["name"]).exists())

        # Проверка, что автор задачи - текущий пользователь
        new_task = Task.objects.get(name=new_task_data["name"])
        self.assertEqual(new_task.author, self.user)

    def test_task_detail_view_success(self):
        """Проверяет доступность и шаблон детальной страницы задачи."""
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/detail.html")
        self.assertContains(response, self.task_data["name"])
        self.assertContains(response, self.task_data["description"])

    def test_task_update_view_get_success(self):
        """Проверяет доступность и шаблон страницы редактирования задачи."""
        response = self.client.get(self.task_update_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/update.html")
        self.assertContains(response, self.task_data["name"])

    def test_task_update_view_post_success(self):
        """Проверяет успешное обновление задачи."""
        updated_data = {
            "name": "Updated Task Name",
            "description": "Updated Description",
            "status": self.status.pk,
            "executor": self.user.pk,  # Меняем исполнителя
        }
        response = self.client.post(self.task_update_url, data=updated_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)

        # Проверка, что данные обновились
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, updated_data["name"])
        self.assertEqual(self.task.description, updated_data["description"])
        self.assertEqual(self.task.executor, self.user)

    def test_task_delete_view_get_success(self):
        """Проверяет доступ к странице подтверждения удаления задачи."""
        response = self.client.get(self.task_delete_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/delete.html")
        self.assertContains(response, self.task_data["name"])

    def test_task_delete_view_post_success(self):
        """Проверяет успешное удаление задачи."""
        task_pk_to_delete = self.task.pk
        initial_task_count = Task.objects.count()
        response = self.client.post(self.task_delete_url)

        # Проверка, что произошел редирект
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)

        # Проверка, что задача удалена
        task_exists_after_delete = Task.objects.filter(
            pk=task_pk_to_delete
        ).exists()
        self.assertFalse(
            task_exists_after_delete,
            "Задача не была удалена из БД"
        )
        self.assertEqual(
            Task.objects.count(),
            initial_task_count - 1,
            "Количество задач не уменьшилось"
        )

    def test_task_delete_view_not_author_forbidden(self):
        """Проверяет, что не автор не может удалить задачу."""
        # Создаем задачу от другого пользователя
        other_task = Task.objects.create(
            name="Other Task",
            description="Other Description",
            status=self.status,
            author=self.other_user,
            executor=self.user,
        )
        other_task_delete_url = reverse("tasks:delete", args=[other_task.pk])

        # Логинимся от имени текущего пользователя (не автора задачи)
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )

        # Пытаемся удалить задачу
        response = self.client.post(other_task_delete_url)

        # Проверка, что произошел редирект (запрещено)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)

        # Проверка, что задача не удалена
        self.assertTrue(
            Task.objects.filter(pk=other_task.pk).exists(),
            "Задача была удалена не автором"
        )

    # --- НОВЫЕ ТЕСТЫ ДЛЯ ФИЛЬТРАЦИИ ---
    def test_task_filter_by_status(self):
        """Проверяет фильтрацию задач по статусу."""
        # Создаем второй статус
        another_status = Status.objects.create(name="Another Status")

        # Создаем еще одну задачу с другим статусом
        Task.objects.create(
            name="Task with different status",
            description="Description",
            status=another_status,
            author=self.user,
        )

        # Формируем URL с параметром фильтрации по статусу
        filter_url = f"{self.tasks_index_url}?status={self.status.pk}"
        # Отправляем GET-запрос
        response = self.client.get(filter_url)

        # Проверяем, что страница загрузилась успешно
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # Проверяем, что в контенте есть имя нашей первой задачи
        self.assertContains(response, self.task_data["name"])
        # Проверяем, что в контенте НЕТ имени задачи с другим статусом
        self.assertNotContains(response, "Task with different status")

    def test_task_filter_by_executor(self):
        """Проверяет фильтрацию задач по исполнителю."""
        # Создаем задачу без исполнителя
        task_without_executor = Task.objects.create(
            name="Task without executor",
            description="Description",
            status=self.status,
            author=self.user,
            # executor не указан (None)
        )

        # Формируем URL с параметром фильтрации по исполнителю (other_user)
        filter_url = f"{self.tasks_index_url}?executor={self.other_user.pk}"
        response = self.client.get(filter_url)

        # Проверяем успешность запроса
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # Проверяем, что задача с исполнителем other_user найдена
        self.assertContains(response, self.task_data["name"])
        # Проверяем, что задача без исполнителя НЕ найдена
        self.assertNotContains(response, task_without_executor.name)

    def test_task_filter_by_own_task(self):
        """Проверяет фильтрацию задач по автору (только свои задачи)."""
        # Создаем задачу от другого пользователя
        task_from_another_user = Task.objects.create(
            name="Task from another user",
            description="Description",
            status=self.status,
            author=self.other_user,  # Автор - другой пользователь
        )

        # Формируем URL с параметром фильтрации self_tasks=on
        filter_url = f"{self.tasks_index_url}?self_tasks=on"
        response = self.client.get(filter_url)

        # Проверяем успешность запроса
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # Проверяем, что задача текущего пользователя найдена
        self.assertContains(response, self.task_data["name"])
        # Проверяем, что задача другого пользователя НЕ найдена
        self.assertNotContains(response, task_from_another_user.name)

    def test_task_filter_by_label(self):
        """Проверяет фильтрацию задач по метке."""
        # Создаем метки
        label1 = Label.objects.create(name="Label 1")
        label2 = Label.objects.create(name="Label 2")

        # Добавляем первую метку к существующей задаче
        self.task.labels.add(label1)

        # Создаем новую задачу и добавляем ей вторую метку
        task_with_label2 = Task.objects.create(
            name="Task with label 2",
            description="Description",
            status=self.status,
            author=self.user,
        )
        task_with_label2.labels.add(label2)

        # Формируем URL с параметром фильтрации по первой метке
        filter_url = f"{self.tasks_index_url}?labels={label1.pk}"
        response = self.client.get(filter_url)

        # Проверяем успешность запроса
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        # Проверяем, что задача с первой меткой найдена
        self.assertContains(response, self.task_data["name"])
        # Проверяем, что задача со второй меткой НЕ найдена
        self.assertNotContains(response, task_with_label2.name)
