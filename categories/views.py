from rest_framework import viewsets

from .models import Category
from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Category.objects.order_by("name").filter(user__pk=self.request.user.id)
