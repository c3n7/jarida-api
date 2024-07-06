from rest_framework import serializers

from .models import JournalEntry, JournalEntryCategory
from categories.models import Category


class JournalEntrySerializer(serializers.ModelSerializer):
    categories = serializers.StringRelatedField(many=True, read_only=True)

    category_names = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=20),
        allow_empty=True,
        write_only=True,
    )

    class Meta:
        fields = (
            "id",
            "title",
            "content",
            "date",
            "created_at",
            "categories",
            "category_names",
        )
        model = JournalEntry

    def create(self, validated_data):
        user = validated_data.get("user")

        journal_entry = JournalEntry.objects.create(
            title=validated_data.get("title"),
            content=validated_data.get("content"),
            date=validated_data.get("date"),
            user_id=user.pk,
        )

        for category_name in validated_data.get("category_names", []):
            category, _ = Category.objects.get_or_create(
                name=category_name,
                user_id=user.pk,
            )
            JournalEntryCategory.objects.get_or_create(
                category_id=category.pk,
                journal_entry_id=journal_entry.pk,
            )

        return journal_entry
