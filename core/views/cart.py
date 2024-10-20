from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import AtomicMixin
from ..serializers.cart_item import CartItemSerializer, UpdateItemSerializer, \
    RemoveCartItemSerializer
from ..models.cart import Cart
from ..models.cart_item import CartItem


class AddCartView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CartItemSerializer(data=request.data, context=dict(request=request))
        serializer.is_valid(raise_exception=True)
        cart_item = serializer.save()

        data = cart_item.cart.get_cart_data()
        return Response(data=data, status=status.HTTP_201_CREATED)


class UpdateCartView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = UpdateItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart_item = get_object_or_404(
            CartItem,
            cart__id=serializer.data['cart_id'],
            id=serializer.data['cart_id'],
        )
        cart_item.update_quantity(serializer.data['quantity'])
        data = cart_item.cart.get_cart_data()
        return Response(data=data, status=status.HTTP_200_OK)


class RemoveCartView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def get_object(self, cart_id: int):
        cart = get_object_or_404(Cart, id=cart_id)
        return cart

    def delete(self, request, *args, **kwargs):
        serializer = RemoveCartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self.get_object(serializer.data['cart_id'])
        cart.remove_item(serializer.data['cart_item_id'])
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # instance = self.request.user.carts.filter(status='open').first()
        instance = get_object_or_404(
            Cart,
            user=self.request.user,
            status='open'
        )

        data = instance.get_cart_data()
        return Response(data=data, status=status.HTTP_200_OK)

