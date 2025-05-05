import http
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from statuses.models import Status
from tasks.models import Task
from .models import Label
from django.utils.translation import gettext_lazy as _


class LabelViewsTests(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestPassword123!",
        }
        self.user = User.objects.create_user(**self.user_data)

        self.label_data = {
            "name": "Test Label",
        }
        self.label = Label.objects.create(**self.label_data)

        self.status = Status.objects.create(name="Test Status")

        self.task = Task.objects.create(
            name="Task with label",
            description="Test Description",
            status=self.status,
            author=self.user,
        )
        self.task.labels.add(self.label)

        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )

        self.labels_index_url = reverse("labels:index")
        self.label_create_url = reverse("labels:create")
        self.label_update_url = reverse("labels:update", args=[self.label.pk])
        self.label_delete_url = reverse("labels:delete", args=[self.label.pk])
        self.login_url = reverse("login")

    def test_labels_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.labels_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertEqual(response.url.split("?")[0], self.login_url)

    def test_labels_list_view_success(self):
        response = self.client.get(self.labels_index_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "labels/index.html")
        self.assertContains(response, self.label_data["name"])

    def test_label_create_view_get(self):
        response = self.client.get(self.label_create_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "labels/create.html")

    def test_label_create_view_post_success(self):
        new_label_data = {
            "name": "New Test Label",
        }
        response = self.client.post(self.label_create_url, data=new_label_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.labels_index_url)
        self.assertTrue(Label.objects.filter(name=new_label_data["name"]).exists())

    def test_label_update_view_get_success(self):
        response = self.client.get(self.label_update_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "labels/update.html")
        self.assertContains(response, self.label_data["name"])

    def test_label_update_view_post_success(self):
        updated_data = {
            "name": "Updated Label Name",
        }
        response = self.client.post(self.label_update_url, data=updated_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.labels_index_url)

        self.label.refresh_from_db()
        self.assertEqual(self.label.name, updated_data["name"])

    def test_label_delete_view_get_success(self):
        new_label = Label.objects.create(name="Label to Delete")
        delete_url = reverse("labels:delete", args=[new_label.pk])

        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "labels/delete.html")
        self.assertContains(response, new_label.name)

    def test_label_delete_view_post_success(self):
        new_label = Label.objects.create(name="Label to Delete")
        delete_url = reverse("labels:delete", args=[new_label.pk])

        label_pk_to_delete = new_label.pk
        initial_label_count = Label.objects.count()
        response = self.client.post(delete_url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.labels_index_url)

        label_exists_after_delete = Label.objects.filter(
            pk=label_pk_to_delete
        ).exists()
        self.assertFalse(
            label_exists_after_delete,
            "Label was not deleted from the DB"
        )
        self.assertEqual(
            Label.objects.count(),
            initial_label_count - 1,
            "The number of labels did not decrease"
        )

    def test_label_delete_protected_when_used(self):
        response = self.client.post(self.label_delete_url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, self.labels_index_url)

        self.assertTrue(
            Label.objects.filter(pk=self.label.pk).exists(),
            "Label was deleted, although it is associated with tasks"
        )
