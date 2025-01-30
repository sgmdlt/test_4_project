from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.utils import get_test_data, identity


class LabelTest(TestCase):
    fixtures = ["users.json", "labels.json"]

    @classmethod
    def setUpTestData(cls):
        cls.test_data = get_test_data()

    def setUp(self):
        exist_user_data = self.test_data["users"]["existing"]
        self.client.login(
            username=exist_user_data["username"],
            password=exist_user_data["password"],
        )

    def assertLabel(self, label, label_data):
        self.assertEqual(label.__str__(), label_data["name"])
        self.assertEqual(label.name, label_data["name"])

    def test_index_page(self):
        response = self.client.get(reverse("labels:index"))
        self.assertEqual(response.status_code, 200)

        labels = Label.objects.all()
        self.assertQuerysetEqual(
            response.context["label_list"],
            labels,
            transform=identity,
            ordered=False,
        )

    def test_create_page(self):
        response = self.client.get(reverse("labels:create"))
        self.assertEqual(response.status_code, 200)

    def test_create(self):
        new_label_data = self.test_data["labels"]["new"]
        response = self.client.post(reverse("labels:create"), new_label_data)

        self.assertRedirects(response, reverse("labels:index"))
        created_label = Label.objects.get(name=new_label_data["name"])
        self.assertLabel(created_label, new_label_data)

    def test_update_page(self):
        exist_label_data = self.test_data["labels"]["existing"]
        exist_label = Label.objects.get(name=exist_label_data["name"])
        response = self.client.get(
            reverse("labels:update", args=[exist_label.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_update(self):
        exist_label_data = self.test_data["labels"]["existing"]
        new_label_data = self.test_data["labels"]["new"]
        exist_label = Label.objects.get(name=exist_label_data["name"])
        response = self.client.post(
            reverse("labels:update", args=[exist_label.pk]),
            new_label_data,
        )

        self.assertRedirects(response, reverse("labels:index"))
        updated_label = Label.objects.get(name=new_label_data["name"])
        self.assertLabel(updated_label, new_label_data)

    def test_delete_page(self):
        exist_label_data = self.test_data["labels"]["existing"]
        exist_label = Label.objects.get(name=exist_label_data["name"])
        response = self.client.get(
            reverse("labels:delete", args=[exist_label.pk])
        )

        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        exist_label_data = self.test_data["labels"]["existing"]
        exist_label = Label.objects.get(name=exist_label_data["name"])
        response = self.client.post(
            reverse("labels:delete", args=[exist_label.pk])
        )

        self.assertRedirects(response, reverse("labels:index"))
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(name=exist_label_data["name"])
