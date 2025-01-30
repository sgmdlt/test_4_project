from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.statuses.models import TaskStatus
from task_manager.utils import get_test_data, identity


class TaskStatusTest(TestCase):
    fixtures = ["users.json", "task_statuses.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def setUp(self):
        exist_user_data = self.test_data["users"]["existing"]
        self.client.login(
            username=exist_user_data["username"],
            password=exist_user_data["password"],
        )

    def assertTaskStatus(self, status, status_data):
        self.assertEqual(status.__str__(), status_data["name"])
        self.assertEqual(status.name, status_data["name"])

    def test_index_page(self):
        response = self.client.get(reverse("statuses:index"))
        self.assertEqual(response.status_code, 200)

        statuses = TaskStatus.objects.all()
        self.assertQuerysetEqual(
            response.context["taskstatus_list"],
            statuses,
            transform=identity,
            ordered=False,
        )

    def test_create_page(self):
        response = self.client.get(reverse("statuses:create"))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        new_status_data = self.test_data["statuses"]["new"]
        response = self.client.post(reverse("statuses:create"), new_status_data)

        self.assertRedirects(response, reverse("statuses:index"))
        created_status = TaskStatus.objects.get(name=new_status_data["name"])
        self.assertTaskStatus(created_status, new_status_data)

    def test_update_page(self):
        exist_status_data = self.test_data["statuses"]["existing"]
        exist_status = TaskStatus.objects.get(name=exist_status_data["name"])
        response = self.client.get(
            reverse("statuses:update", args=[exist_status.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_update(self):
        exist_status_data = self.test_data["statuses"]["existing"]
        new_status_data = self.test_data["statuses"]["new"]
        exist_status = TaskStatus.objects.get(name=exist_status_data["name"])
        response = self.client.post(
            reverse("statuses:update", args=[exist_status.pk]),
            new_status_data,
        )

        self.assertRedirects(response, reverse("statuses:index"))
        updated_status = TaskStatus.objects.get(name=new_status_data["name"])
        self.assertTaskStatus(updated_status, new_status_data)

    def test_delete_page(self):
        exist_status_data = self.test_data["statuses"]["existing"]
        exist_status = TaskStatus.objects.get(name=exist_status_data["name"])
        response = self.client.get(
            reverse("statuses:delete", args=[exist_status.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        exist_status_data = self.test_data["statuses"]["existing"]
        exist_status = TaskStatus.objects.get(name=exist_status_data["name"])
        response = self.client.post(
            reverse("statuses:delete", args=[exist_status.pk])
        )

        self.assertRedirects(response, reverse("statuses:index"))
        with self.assertRaises(ObjectDoesNotExist):
            TaskStatus.objects.get(name=exist_status_data["name"])
