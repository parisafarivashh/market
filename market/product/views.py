from rest_framework.generics import ListAPIView, GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Product, Detail
from .serializers import ProductSerializer, CreateProductSerializer, \
    DetailSerializer
from user.filtering import IsOwnerProductFilterBackend


class ListAllProducts(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'sub_category', 'seller_id']
    search_fields = ['name', 'sub_category', '^seller_id__username']
    ordering_fields = ['id', 'name', 'sub_category', 'seller_id__username']
    ordering = ['name']


class ListProductOfSeller(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    filter_backends = [IsOwnerProductFilterBackend]


class CreateProductAPI(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        details = request.data.pop('details')
        serializer = CreateProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data
        product.update(seller_id=self.request.user)
        product = Product.objects.create(**product)

        # Todo : many true added and create bulky
        for detail in details:
            serializer_detail = DetailSerializer(data=detail)
            serializer_detail.is_valid(raise_exception=True)
            serializer_detail.validated_data['product_id'] = product
            Detail.objects.create(**serializer_detail.validated_data)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
