from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..filterset import CategoryFilter
from ..models.category import Category
from ..serializers.category import CategoryListCreateSerializer
from .mixins import AtomicMixin


class CategoryListCreateApiView(generics.ListCreateAPIView, AtomicMixin):
    serializer_class = CategoryListCreateSerializer
    django_filters = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    def get_permissions(self):
        permission_classes = [IsAuthenticated()]
        if self.request.method == 'Post':
            permission_classes = [IsAuthenticated(), IsAdminUser()]

        return permission_classes


    def get_queryset(self):
        removed_at = self.request.query_params.get('removed_at')
        query = Category.objects.filter(parent__isnull=True)
        if removed_at is not None and removed_at.lower() == 'true':
            return query.removed()

        return query.not_removed()
