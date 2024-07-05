from rest_framework import serializers

from .models import JournalEntry, JournalEntryCategory
from categories.models import Category


class JournalEntrySerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        fields = (
            "id",
            "title",
            "content",
            "date",
            "created_at",
            "categories",
        )
        model = JournalEntry


class JournalEntryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "user",
            "category",
        )
