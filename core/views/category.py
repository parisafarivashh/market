from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models.category import Category
from ..serializers.category import CategoryListCreateSerializer


class CategoryListCreateApiView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = CategoryListCreateSerializer

    def get_queryset(self):
        removed_at = self.request.query_params.get('removed_at')
        if removed_at is not None and removed_at.lower() == 'true':
            return Category.objects.removed()

        return Category.objects.not_removed()
