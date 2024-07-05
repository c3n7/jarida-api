from django.contrib.auth import get_user_model
from django.test import TestCase

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
