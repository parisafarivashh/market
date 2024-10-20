from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from ..filterset import CartFilter
from ..models.cart import Cart
from ..serializers.cart import CartDetailsSerializer


class OrderView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CartFilter

    def get_queryset(self):
        return Cart.objects.done_status().filter(user=self.request.user)

