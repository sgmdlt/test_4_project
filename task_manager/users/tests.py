from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.utils import get_test_data, identity


class UserTest(TestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def login(self):
        exist_user_data = self.test_data["users"]["existing"]
        self.client.login(
            username=exist_user_data["username"],
            password=exist_user_data["password"],
        )

    def assertUser(self, user, user_data):
        self.assertEqual(user.__str__(), user_data["full_name"])
        self.assertEqual(user.first_name, user_data["first_name"])
        self.assertEqual(user.last_name, user_data["last_name"])
        self.assertEqual(user.username, user_data["username"])

    def test_index_page(self):
        response = self.client.get(reverse("users:index"))
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        self.assertQuerysetEqual(
            response.context["user_list"],
            users,
            transform=identity,
            ordered=False,
        )

    def test_create_page(self):
        response = self.client.get(reverse("users:create"))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        new_user_data = self.test_data["users"]["new"]
        response = self.client.post(reverse("users:create"), new_user_data)

        self.assertRedirects(response, reverse("login"))
        created_user = get_user_model().objects.get(
            username=new_user_data["username"]
        )
        self.assertUser(created_user, new_user_data)

    def test_update_page(self):
        exist_user_data = self.test_data["users"]["existing"]
        self.login()

        exist_user = get_user_model().objects.get(
            username=exist_user_data["username"]
        )
        response = self.client.get(
            reverse("users:update", args=[exist_user.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_update(self):
        exist_user_data = self.test_data["users"]["existing"]
        new_user_data = self.test_data["users"]["new"]
        self.login()

        exist_user = get_user_model().objects.get(
            username=exist_user_data["username"]
        )
        response = self.client.post(
            reverse("users:update", args=[exist_user.pk]),
            new_user_data,
        )

        self.assertRedirects(response, reverse("users:index"))
        updated_user = get_user_model().objects.get(
            username=new_user_data["username"]
        )
        self.assertUser(updated_user, new_user_data)

    def test_delete_page(self):
        exist_user_data = self.test_data["users"]["existing"]
        self.login()

        exist_user = get_user_model().objects.get(
            username=exist_user_data["username"]
        )
        response = self.client.get(
            reverse("users:delete", args=[exist_user.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        exist_user_data = self.test_data["users"]["existing"]
        self.login()

        exist_user = get_user_model().objects.get(
            username=exist_user_data["username"]
        )
        response = self.client.post(
            reverse("users:delete", args=[exist_user.pk])
        )

        self.assertRedirects(response, reverse("users:index"))
        with self.assertRaises(ObjectDoesNotExist):
            get_user_model().objects.get(username=exist_user_data["username"])
