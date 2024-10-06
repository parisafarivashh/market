from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db import transaction
from ..models import Attribute
from ..models.product import Product
from ..models.variant import Variant
from ..serializers import ProductCreateSerializer, ProductListSerializer, ProductUpdateSerializer
from ..permissions import IsOwn


class ProductListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Product.objects.filter(removed_at__isnull=True)

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
        serializer.save('creator', self.request.user)


class ProductGetUpdateView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'id'

    def get_queryset(self):
        return Product.objects.filter(removed_at__isnull=True)

    @transaction.atomic()
    def dispatch(self, request, *args, **kwargs):
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

