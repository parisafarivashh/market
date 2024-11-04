from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db import transaction

from market.utility import delete_cache
from ..filterset import ProductFilter
from ..models import Attribute
from ..models.product import Product
from ..models.variant import Variant
from ..serializers import ProductCreateSerializer, ProductListSerializer, ProductUpdateSerializer
from ..permissions import IsOwn
from .mixins import AtomicMixin


class ProductListCreateView(generics.ListCreateAPIView, AtomicMixin):
    key_prefix = 'list_product'
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return Product.objects.select_related('category').filter(removed_at__isnull=True)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'POST':
            return ProductCreateSerializer

        return ProductListSerializer

    def get_permissions(self):
        permission_class = [AllowAny()]
        if self.request.method == 'Post':
            permission_class = [IsAuthenticated()]

        return permission_class

    def perform_create(self, serializer):
        delete_cache(self.key_prefix)
        serializer.save(creator=self.request.user)

    @method_decorator(cache_page(300, key_prefix=key_prefix))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductGetUpdateView(generics.RetrieveUpdateDestroyAPIView, AtomicMixin):
    key_prefix = 'list_product'
    lookup_field = 'id'

    def get_queryset(self):
        return Product.objects.select_related('category').filter(removed_at__isnull=True)

    @transaction.atomic()
    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in ['put', 'patch', 'delete']:
            delete_cache(self.key_prefix)
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permission_class = [IsAuthenticated()]
        if self.request.method == 'UPDATE':
            permission_class = [IsAuthenticated(), IsOwn()]

        if self.request.method == 'DELETE':
            permission_class = [IsAuthenticated(), IsAdminUser()]

        return permission_class

    def get_serializer_class(self):
        serializer_class = ProductListSerializer
        if self.request.method in ['PATCH', 'PUT', 'UPDATE']:
            serializer_class = ProductUpdateSerializer

        return serializer_class

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        Variant.objects.filter(product=product).delete()
        Attribute.objects.filter(product=product).delete()
        self.perform_destroy(product)

        return Response(status=status.HTTP_204_NO_CONTENT)

