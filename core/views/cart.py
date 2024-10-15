from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import AtomicMixin
from ..serializers.cart import CartDetailsSerializer
from ..serializers.cart_item import CartItemSerializer, CartItemListSerializer
from ..models.cart_item import CartItem
from ..models.cart import Cart


class AddCartView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data, context=dict(request=request))
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()

        cart_data = CartDetailsSerializer(instance=cart_item.cart).data
        cart_items = CartItem.objects.filter(cart=cart_item.cart)
        cart_items_data = CartItemListSerializer(cart_items, many=True).data

        return Response(data=dict(cart=cart_data, cart_items=cart_items_data), status=status.HTTP_201_CREATED)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Cart,
            user=self.request.user,
            status='open'
        )
        cart_data = CartDetailsSerializer(instance).data

        cart_items = CartItem.objects.filter(cart=instance)
        cart_items_data = CartItemListSerializer(cart_items, many=True).data
        data = dict(cart=cart_data, card_items=cart_items_data)

        return Response(data=data, status=status.HTTP_200_OK)

