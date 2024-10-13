from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from ..models.attribute import Attribute
from ..serializers.attribute import AttributeSerializer
from .mixins import AtomicMixin


class AttributeCreateView(generics.CreateAPIView, AtomicMixin):
    serializer_class = AttributeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Attribute.objects.not_removed()

    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_id'])

