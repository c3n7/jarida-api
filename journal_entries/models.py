from django.db import models
from django.conf import settings

from categories.models import Category


class JournalEntry(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "journal entries"

    def __str__(self) -> str:
        return f"{self.title} - {self.user.username}"


class JournalEntryCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    journal_entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "journal entry categories"

    def __str__(self) -> str:
        return f"{self.category.name} - {self.journal_entry.title}"
