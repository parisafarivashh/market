from django.db.models import Q
from rest_framework import response, status
from rest_framework.generics import CreateAPIView, UpdateAPIView, \
    RetrieveUpdateDestroyAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated

from order.serializers import ItemOrderSerializer, UpdateItemOrderSerializer, ListOrderSerializer
from order.models import ItemOrder, Order


class CreateItemOrder(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemOrderSerializer
    queryset = ItemOrder.objects.all()

    def perform_create(self, serializer):
        serializer.save(order=self.request.user.order)


# class CreateItemOrder(GenericAPIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         order = self.request.user.order
#         serializer = ItemOrderSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.validated_data['order'] = order
#         item = ItemOrder
#         ItemOrder.objects.create(**serializer.validated_data)


class UpdateMyOrder(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateItemOrderSerializer
    queryset = ItemOrder.objects.all()
    lookup_field = 'id'


class ListOrderUser(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListOrderSerializer

    def get_queryset(self):
        return Order.objects.filter(id=self.request.user.order.id)