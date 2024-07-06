from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from categories.models import Category
from .models import JournalEntry, JournalEntryCategory


class JournalEntryTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = get_user_model().objects.create_user(
            username="JohnDoe", password="secret"
        )

        cls.journal_entry = JournalEntry.objects.create(
            user=cls.user,
            title="Foo",
            content="Bar",
            date="2024-07-05",
        )

        for i in range(3):
            category = Category.objects.create(user=cls.user, name=f"category_no_{i}")
            JournalEntryCategory.objects.create(
                journal_entry_id=cls.journal_entry.pk,
                category_id=category.pk,
            )

    def test_category_model(self):
        self.assertEqual(self.journal_entry.user.username, "JohnDoe")
        self.assertEqual(self.journal_entry.title, "Foo")
        self.assertEqual(self.journal_entry.content, "Bar")
        self.assertEqual(self.journal_entry.date, "2024-07-05")
        self.assertEqual(len(self.journal_entry.categories.all()), 3)
