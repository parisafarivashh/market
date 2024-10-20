from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from ..serializers.cart import CartDetailsSerializer
from ..serializers.cart_item import CartItemSerializer, RemoveCartItemSerializer, \
    CartItemListSerializer
from ..models.cart import Cart
from ..models.cart_item import CartItem


class AddCartCommand:

    def execute(self, request):
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()

        cart_data = CartDetailsSerializer(cart_item.cart).data
        cart_items_data = CartItemListSerializer(
            CartItem.objects.filter(cart=cart_item.cart), many=True
        ).data

        return dict(cart=cart_data, cart_items=cart_items_data), status.HTTP_201_CREATED


class RemoveCartCommand:

    def execute(self, request):
        serializer = RemoveCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart = get_object_or_404(Cart, id=serializer.data['cart_id'])
        CartItem.objects.filter(
            id=serializer.data['cart_item_id'],
            cart=cart.id
        ).delete()

        return {'message': 'Cart item removed successfully'}, status.HTTP_204_NO_CONTENT


class GetCartCommand:

    def execute(self, request):
        cart = get_object_or_404(Cart, user=request.user, status='open')
        cart_data = CartDetailsSerializer(cart).data
        cart_items_data = CartItemListSerializer(
            CartItem.objects.filter(cart=cart), many=True
        ).data

        return dict(cart=cart_data, cart_items=cart_items_data), status.HTTP_200_OK

