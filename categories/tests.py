import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Category


class CategoryTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username="JohnDoe", password="secret"
        )

        cls.category = Category.objects.create(user=cls.user, name="reflections")

    def test_category_model(self):
        self.assertEqual(self.category.user.username, "JohnDoe")
        self.assertEqual(self.category.name, "reflections")


class CategoryViewSetTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = get_user_model().objects.create_user(
            username="JohnDoe", password="secret"
        )

        cls.user_2 = get_user_model().objects.create_user(
            username="JaneDoe", password="secret"
        )

    def test_can_list_categories(self):
        Category.objects.create(user=self.user_1, name="meditations")
        Category.objects.create(user=self.user_1, name="mantras")
        Category.objects.create(user=self.user_2, name="reflections")

        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.get("/api/v1/categories")

        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "meditations")
        self.assertEqual(response.data[1]["name"], "mantras")

    def test_can_create_category(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.post(
            "/api/v1/categories", {"name": "meditations"}, format="json"
        )

        self.assertEqual(response.data["name"], "meditations")

        categories = Category.objects.filter(name="meditations")
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].name, "meditations")
        self.assertEqual(categories[0].user.username, "JohnDoe")
