import http
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from labels.models import Label
from statuses.models import Status
from .models import Task
from django.utils.translation import gettext_lazy as _


class TaskViewsTests(TestCase):

    def setUp(self):
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

        self.status = Status.objects.create(name="Test Status")

        self.task_data = {
            "name": "Test Task",
            "description": "Test Description",
            "status": self.status,
            "author": self.user,
            "executor": self.other_user,
        }
        self.task = Task.objects.create(**self.task_data)

        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )

        self.tasks_index_url = reverse("tasks:index")
        self.task_create_url = reverse("tasks:create")
        self.task_detail_url = reverse("tasks:detail", args=[self.task.pk])
        self.task_update_url = reverse("tasks:update", args=[self.task.pk])
        self.task_delete_url = reverse("tasks:delete", args=[self.task.pk])
        self.login_url = reverse("login")

    def test_tasks_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.tasks_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(response.url.split("?")[0], self.login_url)

    def test_tasks_list_view_success(self):
        response = self.client.get(self.tasks_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/index.html")
        self.assertContains(response, self.task_data["name"])

    def test_task_create_view_get(self):
        response = self.client.get(self.task_create_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/create.html")

    def test_task_create_view_post_success(self):
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

        new_task = Task.objects.get(name=new_task_data["name"])
        self.assertEqual(new_task.author, self.user)

    def test_task_detail_view_success(self):
        response = self.client.get(self.task_detail_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/detail.html")
        self.assertContains(response, self.task_data["name"])
        self.assertContains(response, self.task_data["description"])

    def test_task_update_view_get_success(self):
        response = self.client.get(self.task_update_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/update.html")
        self.assertContains(response, self.task_data["name"])

    def test_task_update_view_post_success(self):
        updated_data = {
            "name": "Updated Task Name",
            "description": "Updated Description",
            "status": self.status.pk,
            "executor": self.user.pk,
        }
        response = self.client.post(self.task_update_url, data=updated_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)

        self.task.refresh_from_db()
        self.assertEqual(self.task.name, updated_data["name"])
        self.assertEqual(self.task.description, updated_data["description"])
        self.assertEqual(self.task.executor, self.user)

    def test_task_delete_view_get_success(self):
        response = self.client.get(self.task_delete_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "tasks/delete.html")
        self.assertContains(response, self.task_data["name"])

    def test_task_delete_view_post_success(self):
        task_pk_to_delete = self.task.pk
        initial_task_count = Task.objects.count()
        response = self.client.post(self.task_delete_url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.tasks_index_url)

        task_exists_after_delete = Task.objects.filter(
            pk=task_pk_to_delete
        ).exists()
        self.assertFalse(
            task_exists_after_delete,
            "Task was not deleted from the DB"
        )
        self.assertEqual(
            Task.objects.count(),
            initial_task_count - 1,
            "The number of tasks did not decrease"
        )

    def test_task_delete_view_not_author_forbidden(self):
        other_task = Task.objects.create(
            name="Other Task",
            description="Other Description",
            status=self.status,
            author=self.other_user,
            executor=self.user,
        )
        other_task_delete_url = reverse("tasks:delete", args=[other_task.pk])

        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )

        response = self.client.post(other_task_delete_url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)

        self.assertTrue(
            Task.objects.filter(pk=other_task.pk).exists(),
            "Task was deleted by non-author"
        )

    def test_task_filter_by_status(self):
        another_status = Status.objects.create(name="Another Status")

        Task.objects.create(
            name="Task with different status",
            description="Description",
            status=another_status,
            author=self.user,
        )

        filter_url = f"{self.tasks_index_url}?status={self.status.pk}"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.task_data["name"])
        self.assertNotContains(response, "Task with different status")

    def test_task_filter_by_executor(self):
        task_without_executor = Task.objects.create(
            name="Task without executor",
            description="Description",
            status=self.status,
            author=self.user,
        )

        filter_url = f"{self.tasks_index_url}?executor={self.other_user.pk}"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.task_data["name"])
        self.assertNotContains(response, task_without_executor.name)

    def test_task_filter_by_own_task(self):
        task_from_another_user = Task.objects.create(
            name="Task from another user",
            description="Description",
            status=self.status,
            author=self.other_user,
        )

        filter_url = f"{self.tasks_index_url}?self_tasks=on"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.task_data["name"])
        self.assertNotContains(response, task_from_another_user.name)

    def test_task_filter_by_label(self):
        label1 = Label.objects.create(name="Label 1")
        label2 = Label.objects.create(name="Label 2")

        self.task.labels.add(label1)

        task_with_label2 = Task.objects.create(
            name="Task with label 2",
            description="Description",
            status=self.status,
            author=self.user,
        )
        task_with_label2.labels.add(label2)

        filter_url = f"{self.tasks_index_url}?labels={label1.pk}"
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertContains(response, self.task_data["name"])
        self.assertNotContains(response, task_with_label2.name)
