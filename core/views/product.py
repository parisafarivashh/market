from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..models.product import Product
from ..serializers import ProductCreateSerializer


class ProductListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        return Product.objects.filter(removed_at__isnull=True)

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'Post':
            return ProductCreateSerializer

        return ''

    def get_permissions(self):
        permission_classes = [AllowAny]
        if self.request.method == 'Post':
            permission_classes = [IsAuthenticated()]

        return permission_classes

    def post(self, request, *args, **kwargs):
        pass