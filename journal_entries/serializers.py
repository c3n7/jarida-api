from rest_framework import serializers

from .models import JournalEntry


class JournalEntrySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "title",
            "content",
            "date",
            "created_at",
        )
        model = JournalEntry
