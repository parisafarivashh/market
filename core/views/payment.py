from datetime import datetime

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F

from ..tasks import notification_payment
from ..views import AtomicMixin
from ..serializers import PaymentFailSerializer, CartDetailsSerializer
from ..models.cart import Cart


class PaymentView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            cart = self.request.user.carts.select_for_update().filter(status='open').first()
            _cart_items = cart.cartItems.filter(variant__number__lt=F('quantity'))

            list_cart_items = list(_cart_items)
            data = PaymentFailSerializer(list_cart_items, many=True).data
            #ToDo send notif to user
            _cart_items.delete()

            cart_items = cart.cartItems.filter(variant__number__gte=F('quantity'))
            if cart_items.count() == 0:
                return Response(
                    data=dict(message='One or more items were removed from your cart due to insufficient stock.', data=data),
                    status=status.HTTP_400_BAD_REQUEST
                )

            cart.status = 'done'
            cart.order_date = datetime.today().date()
            cart.save(update_fields=['status', 'order_date'])

            for cart_item in cart_items:
                cart_item.variant.decrease_numer(cart_item.quantity)

            data = CartDetailsSerializer(cart).data
            Cart.objects.create(status='open', user=self.request.user)
            notification_payment.apply_async(args=(cart.id,))
            return Response(data=data, status=status.HTTP_200_OK)

