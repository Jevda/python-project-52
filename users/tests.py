import http
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class UserViewsTests(TestCase):

    def setUp(self):
        self.user_data = {
            "username": "testuser_existing",
            "first_name": "CurrentFirstName",
            "last_name": "CurrentLastName",
            "password": "TestPassword123!",
        }
        self.user = User.objects.create_user(**self.user_data)

        self.other_user_data = {
            "username": "other_user",
            "first_name": "OtherFirst",
            "last_name": "OtherLast",
            "password": "OtherPassword456!",
        }
        self.other_user = User.objects.create_user(**self.other_user_data)

        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )

        self.update_url = reverse("users:update", args=[self.user.pk])
        self.delete_url = reverse("users:delete", args=[self.user.pk])
        self.other_update_url = reverse(
            "users:update",
            args=[self.other_user.pk]
        )
        self.other_delete_url = reverse(
            "users:delete",
            args=[self.other_user.pk]
        )

    def test_user_list_view(self):
        url = reverse("users:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/index.html")

    def test_user_create_view_get(self):
        url = reverse("users:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/create.html")

    def test_user_create_view_post_success(self):
        url_create = reverse("users:create")
        url_login = reverse("login")
        new_user_data = {
            "first_name": "NewFirstName",
            "last_name": "NewLastName",
            "username": "newtestuser999",
            "password1": "NewPassword123!",
            "password2": "NewPassword123!",
        }
        response = self.client.post(url_create, data=new_user_data)
        user_exists = User.objects.filter(
            username=new_user_data["username"]
        ).exists()
        self.assertTrue(user_exists, "User was not created in the DB")
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, url_login)

    def test_user_update_view_get_self(self):
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/update.html")

    def test_user_update_view_get_other_user_forbidden(self):
        response = self.client.get(self.other_update_url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:index"))

    def test_user_update_view_post_self_success(self):
        updated_data = {
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "username": "testuser_existing",
        }
        response = self.client.post(self.update_url, data=updated_data)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:index"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, updated_data["first_name"])
        self.assertEqual(self.user.last_name, updated_data["last_name"])

    def test_user_delete_view_get_self(self):
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertTemplateUsed(response, "users/delete.html")

    def test_user_delete_view_get_other_user_forbidden(self):
        response = self.client.get(self.other_delete_url)
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:index"))

    def test_user_delete_view_post_self_success(self):
        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:index"))

        user_exists_after_delete = User.objects.filter(
            pk=self.user.pk
        ).exists()
        self.assertFalse(
            user_exists_after_delete,
            "User was not deleted from the DB"
        )

    def test_user_delete_view_post_other_user_forbidden(self):
        initial_user_count = User.objects.count()
        response = self.client.post(self.other_delete_url)

        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:index"))

        other_user_exists = User.objects.filter(
            pk=self.other_user.pk
        ).exists()
        self.assertTrue(
            other_user_exists,
            "Other user was deleted, although they should not have been"
        )

        self.assertEqual(
            User.objects.count(),
            initial_user_count,
            "Total number of users changed"
        )
