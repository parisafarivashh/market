from rest_framework import generics
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models import Variant
from ..serializers.variant import VariantCreateSerializer


class VariantListCreateView(generics.ListCreateAPIView):
    serializer_class = VariantCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Variant.objects.not_removed()


class VariantDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VariantCreateSerializer
    queryset = Variant.objects.not_removed()
    lookup_field = 'id'


    def get_permissions(self):
        permission_class = [IsAuthenticated()]
        if self.request.method == 'DELETE':
            permission_class = [IsAuthenticated(), IsAdminUser()]
        return permission_class
