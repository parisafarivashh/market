from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from market.utility import delete_cache
from ..models import Variant
from ..serializers.variant import VariantSerializer
from .mixins import AtomicMixin


class VariantListCreateView(AtomicMixin, generics.ListCreateAPIView):
    key_prefix = 'list_variant'
    serializer_class = VariantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Variant.objects.not_removed().select_related('product') \
            .filter(product__id=self.kwargs['product_id'])

        return queryset

    def perform_create(self, serializer):
        delete_cache(self.key_prefix)
        serializer.save(product_id=self.kwargs['product_id'])

    @method_decorator(cache_page(300, key_prefix=key_prefix))
    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class VariantDetailsView(AtomicMixin, generics.RetrieveUpdateDestroyAPIView):
    key_prefix = 'list_variant'
    serializer_class = VariantSerializer
    queryset = Variant.objects.not_removed()
    lookup_field = 'id'

    def get_permissions(self):
        permission_class = [IsAuthenticated()]
        if self.request.method == 'DELETE':
            permission_class = [IsAuthenticated(), IsAdminUser()]
        return permission_class

    def delete(self, request, *args, **kwargs):
        delete_cache(self.key_prefix)
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        delete_cache(self.key_prefix)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        delete_cache(self.key_prefix)
        return self.partial_update(request, *args, **kwargs)
