from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..filterset import AttributeFilter
from ..models.attribute import Attribute
from ..serializers.attribute import AttributeSerializer
from .mixins import AtomicMixin


class AttributeCreateView(generics.ListCreateAPIView, AtomicMixin):
    serializer_class = AttributeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Attribute.objects.not_removed() \
            .filter(product__id=self.kwargs['product_id'])

        filter_set = AttributeFilter(
            data=self.request.query_params,
            queryset=queryset
        )
        if filter_set.is_valid():
            queryset = filter_set.qs

        return queryset


    def perform_create(self, serializer):
        serializer.save(product_id=self.kwargs['product_id'])


class AttributeDetailsView(generics.RetrieveUpdateDestroyAPIView, AtomicMixin):
    serializer_class = AttributeSerializer
    queryset = Attribute.objects.not_removed()
    lookup_field = 'id'

    def get_permissions(self):
        permission_class = [IsAuthenticated()]
        if self.request.method == 'DELETE':
            permission_class = [IsAuthenticated(), IsAdminUser()]
        return permission_class

