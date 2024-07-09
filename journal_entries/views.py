from rest_framework import viewsets

from .models import JournalEntry
from .serializers import JournalEntrySerializer


class JournalEntryViewSet(viewsets.ModelViewSet):
    serializer_class = JournalEntrySerializer

    def get_queryset(self):
        return JournalEntry.objects.order_by("-pk").filter(
            user__pk=self.request.user.pk
        )

    def perform_create(self, serializer):
        res = serializer.save(user=self.request.user)
