from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import Variant
from ..serializers.variant import VariantSerializer
from .mixins import AtomicMixin


class VariantListCreateView(generics.ListCreateAPIView, AtomicMixin):
    serializer_class = VariantSerializer
    permission_classes = [IsAuthenticated]
    queryset = Variant.objects.not_removed()

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_id'])


class VariantDetailsView(generics.RetrieveUpdateDestroyAPIView, AtomicMixin):
    serializer_class = VariantSerializer
    queryset = Variant.objects.not_removed()
    lookup_field = 'id'


    def get_permissions(self):
        permission_class = [IsAuthenticated()]
        if self.request.method == 'DELETE':
            permission_class = [IsAuthenticated(), IsAdminUser()]
        return permission_class
