from datetime import datetime, timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction

from ..views import AtomicMixin
from ..serializers import CartDetailsSerializer
from ..models.cart import Cart
from ..models.cart_item import CartItem


class PaymentView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            cart = self.request.user.carts.select_for_update().filter(status='open').first()
            cart.status = 'done'
            cart.order_date = datetime.today().date()
            cart.save(update_fields=['status', 'order_date'])

            cart_items = cart.cartItems.all()
            for cart_item in cart_items:
                cart_item.variant.decrease_numer(cart_item.quantity)

            data = CartDetailsSerializer(cart).data
            Cart.objects.create(status='open', user=self.request.user)
            return Response(data=data, status=status.HTTP_200_OK)

