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


class JournalEntryViewSetTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = get_user_model().objects.create_user(
            username="JohnDoe", password="secret"
        )

        cls.user_2 = get_user_model().objects.create_user(
            username="JaneDoe", password="secret"
        )

    def test_can_list_journal_entries(self):
        journal_1 = JournalEntry.objects.create(
            user=self.user_1,
            title="Foo1",
            content="Bar1",
            date="2024-07-01",
        )
        journal_2 = JournalEntry.objects.create(
            user=self.user_1,
            title="Foo2",
            content="Bar2",
            date="2024-07-02",
        )
        JournalEntry.objects.create(
            user=self.user_2,
            title="Foo3",
            content="Bar3",
            date="2024-07-03",
        )

        for i in range(4):
            JournalEntryCategory.objects.create(
                journal_entry=journal_1,
                category=Category.objects.create(
                    user=self.user_1, name=f"category_no_{i}"
                ),
            )
        for i in range(3):
            JournalEntryCategory.objects.create(
                journal_entry=journal_2,
                category=Category.objects.create(
                    user=self.user_1, name=f"category_no_{i}"
                ),
            )

        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.get("/api/v1/journal_entries/")

        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]["title"], "Foo1")
        self.assertEqual(len(response.data[0]["categories"]), 4)

        self.assertEqual(response.data[1]["title"], "Foo2")
        self.assertEqual(len(response.data[1]["categories"]), 3)

    def test_can_create_category(self):
        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.post(
            "/api/v1/journal_entries/",
            {
                "title": "Foo",
                "content": "Bar",
                "date": "2024-07-05",
                "category_names": ["foo cat", "bar cat"],
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], "Foo")

        journal = JournalEntry.objects.filter(title="Foo")
        self.assertTrue(journal.exists())

        journal = journal[0]
        self.assertEqual(journal.title, "Foo")
        self.assertEqual(len(journal.categories.all()), 2)

    def test_can_show_journal_entry(self):
        journal_1 = JournalEntry.objects.create(
            user=self.user_1,
            title="Foo1",
            content="Bar1",
            date="2024-07-01",
        )

        for i in range(4):
            JournalEntryCategory.objects.create(
                journal_entry=journal_1,
                category=Category.objects.create(
                    user=self.user_1, name=f"category_no_{i}"
                ),
            )

        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.get(f"/api/v1/journal_entries/{journal_1.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Foo1")
        self.assertEqual(len(response.data["categories"]), 4)

    def test_can_update_journal_entry(self):
        old_journal = JournalEntry.objects.create(
            user=self.user_1,
            title="Foo1",
            content="Bar1",
            date="2024-07-01",
        )

        for i in range(4):
            JournalEntryCategory.objects.create(
                journal_entry=old_journal,
                category=Category.objects.create(
                    user=self.user_1, name=f"category_no_{i}"
                ),
            )

        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.put(
            f"/api/v1/journal_entries/{old_journal.pk}/",
            data={
                "title": "Foo2",
                "content": "Bar2",
                "date": "2023-02-02",
                "category_names": ["foo cat"],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Foo2")

        journal = JournalEntry.objects.get(pk=old_journal.pk)
        self.assertEqual(journal.content, "Bar2")
        self.assertEqual(len(journal.categories.all()), 1)
        self.assertEqual(len(Category.objects.all()), 5)

    def test_can_update_journal_entry(self):
        journal = JournalEntry.objects.create(
            user=self.user_1,
            title="Foo1",
            content="Bar1",
            date="2024-07-01",
        )

        client = APIClient()
        client.force_authenticate(user=self.user_1)
        response = client.delete(
            f"/api/v1/journal_entries/{journal.pk}/",
        )

        self.assertEqual(response.status_code, 204)

        journal = JournalEntry.objects.filter(pk=journal.pk)
        self.assertTrue(not journal.exists())
