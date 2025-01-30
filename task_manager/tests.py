from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.utils import get_test_data


class AppTest(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse("root"))
        self.assertEqual(response.status_code, 200)

    def test_wrong_path_page(self):
        response = self.client.get("/wrong-path/")
        self.assertEqual(response.status_code, 404)


class SessionTest(TestCase):
    fixtures = ["users.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def test_login_logout(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

        exist_user_data = self.test_data["users"]["existing"]
        exist_user = get_user_model().objects.get(
            username=exist_user_data["username"]
        )
        response_login = self.client.post(reverse("login"), exist_user_data)
        self.assertRedirects(response_login, reverse("root"))
        self.assertEqual(
            int(self.client.session["_auth_user_id"]), exist_user.pk
        )

        response_logout = self.client.post(reverse("logout"))
        self.assertRedirects(response_logout, reverse("root"))
