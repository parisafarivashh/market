from django.db import transaction
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from .serializers import ItemOrderSerializer, UpdateItemOrderSerializer, ListOrderSerializer
from .models import ItemOrder, Order
from rest_framework.response import Response
from product.models import Detail


class CreateItemOrder(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order = self.request.user.order
        detail = Detail.objects.get(id=request.data['detail'])
        serializer = ItemOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['order'] = order
        serializer.validated_data['price'] = detail.price
        with transaction.atomic():
            try:
                item = ItemOrder.objects.get(Q(detail=request.data['detail']) & Q(order=order))
                item.count += 1
                item.save(update_fields=['count'])
                detail.count = detail.count - 1

            except ItemOrder.DoesNotExist:
                ItemOrder.objects.create(**serializer.validated_data)
                detail.count = detail.count - int(request.data['count'])

            if detail.count < 0:
                raise ValueError('order number not available')
            detail.save(update_fields=['count'])
        return Response(data={"data": "Added successfully"}, status=status.HTTP_201_CREATED)


class UpdateMyItemOrder(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateItemOrderSerializer
    queryset = ItemOrder.objects.all()
    lookup_field = 'id'


class OrderViewList(ReadOnlyModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ListOrderSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Order.objects.filter(Q(user=user) & Q(paid=False))
        return queryset

    @action(detail=False, url_path='paid', methods=['get'])
    def paid(self, request):
        order_id = self.request.user.order.id
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            if order.final_cost > 0:
                order.paid = True
                order.save(update_fields=['paid'])

                user_orders = Order.objects.filter(paid=False)
                if len(user_orders) == 0:
                    Order.objects.create(user=self.request.user)
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, url_path='basket', methods=['get'])
    def basket(self, request):
        user = self.request.user
        basket = Order.objects.filter(paid=True).filter(user=user)
        serializer = self.get_serializer(basket, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
