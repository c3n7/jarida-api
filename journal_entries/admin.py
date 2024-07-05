from django.contrib import admin

from .models import JournalEntry, JournalEntryCategory

admin.site.register(JournalEntry)
admin.site.register(JournalEntryCategory)
