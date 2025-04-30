# tasks/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import http

from .models import Task
from statuses.models import Status


class TaskViewsTests(TestCase):

    def setUp(self):
        """Создаем пользователей, статус и задачи."""
        # Создаем пользователей
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPassword123!',
        }
        self.user = User.objects.create_user(**self.user_data)

        self.other_user_data = {
            'username': 'otheruser',
            'first_name': 'Other',
            'last_name': 'User',
            'password': 'OtherPassword456!',
        }
        self.other_user = User.objects.create_user(**self.other_user_data)

        # Создаем статус
        self.status = Status.objects.create(name='Test Status')

        # Создаем задачу
        self.task_data = {
            'name': 'Test Task',
            'description': 'Test Description',
            'status': self.status,
            'author': self.user,
            'executor': self.other_user,
        }
        self.task = Task.objects.create(**self.task_data)

        # Логиним пользователя
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

        # Сохраняем URL'ы
        self.tasks_index_url = reverse('tasks:index')
        self.task_create_url = reverse('tasks:create')
        self.task_detail_url = reverse('tasks:detail', args=[self.task.pk])
        self.task_update_url = reverse('tasks:update', args=[self.task.pk])
        self.task_delete_url = reverse('tasks:delete', args=[self.task.pk])
        self.login_url = reverse('login')

    def test_tasks_list_view_requires_login(self):
        """Проверяет, что список задач требует логина."""
        self.client.logout()
        response = self.client.get(self.tasks_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(response.url.split('?')[0], self.login_url)

    def test_tasks_list_view_success(self):
        """Проверяет доступность и шаблон списка задач."""
        response = self.client.get(self.tasks_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/index.html')
        self.assertContains(response, self.task_data['name'])

    def test_task_create_view_get(self):
        """Проверяет доступность и шаблон страницы создания задачи."""
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/create.html')

    def test_task_create_view_post_success(self):
        """Проверяет создание задачи и редирект."""
        new_task_data = {
            'name': 'New Test Task',
            'description': 'New Test Description',
            'status': self.status.pk,
            'executor': self.other_user.pk,
        }
        response = self.client.post(self.task_create_url, data=new_task_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)
        self.assertTrue(Task.objects.filter(name=new_task_data['name']).exists())

        # Проверка, что автор задачи - текущий пользователь
        new_task = Task.objects.get(name=new_task_data['name'])
        self.assertEqual(new_task.author, self.user)

    def test_task_detail_view_success(self):
        """Проверяет доступность и шаблон детальной страницы задачи."""
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/detail.html')
        self.assertContains(response, self.task_data['name'])
        self.assertContains(response, self.task_data['description'])

    def test_task_update_view_get_success(self):
        """Проверяет доступность и шаблон страницы редактирования задачи."""
        response = self.client.get(self.task_update_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/update.html')
        self.assertContains(response, self.task_data['name'])

    def test_task_update_view_post_success(self):
        """Проверяет успешное обновление задачи."""
        updated_data = {
            'name': 'Updated Task Name',
            'description': 'Updated Description',
            'status': self.status.pk,
            'executor': self.user.pk,  # Меняем исполнителя
        }
        response = self.client.post(self.task_update_url, data=updated_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)

        # Проверка, что данные обновились
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, updated_data['name'])
        self.assertEqual(self.task.description, updated_data['description'])
        self.assertEqual(self.task.executor, self.user)

    def test_task_delete_view_get_success(self):
        """Проверяет доступ к странице подтверждения удаления задачи."""
        response = self.client.get(self.task_delete_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/delete.html')
        self.assertContains(response, self.task_data['name'])

    def test_task_delete_view_post_success(self):
        """Проверяет успешное удаление задачи."""
        task_pk_to_delete = self.task.pk
        initial_task_count = Task.objects.count()
        response = self.client.post(self.task_delete_url)

        # Проверка, что произошел редирект
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)

        # Проверка, что задача удалена
        task_exists_after_delete = Task.objects.filter(pk=task_pk_to_delete).exists()
        self.assertFalse(task_exists_after_delete, "Задача не была удалена из БД")
        self.assertEqual(Task.objects.count(), initial_task_count - 1, "Количество задач не уменьшилось")

    def test_task_delete_view_not_author_forbidden(self):
        """Проверяет, что не автор не может удалить задачу."""
        # Создаем задачу от другого пользователя
        other_task = Task.objects.create(
            name='Other Task',
            description='Other Description',
            status=self.status,
            author=self.other_user,
            executor=self.user,
        )
        other_task_delete_url = reverse('tasks:delete', args=[other_task.pk])

        # Логинимся от имени текущего пользователя (не автора задачи)
        self.client.login(
            username=self.user_data['username'],
            password=self.user_data['password']
        )

        # Пытаемся удалить задачу
        response = self.client.post(other_task_delete_url)

        # Проверка, что произошел редирект (запрещено)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)

        # Проверка, что задача не удалена
        self.assertTrue(Task.objects.filter(pk=other_task.pk).exists(), "Задача была удалена не автором")
