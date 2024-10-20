from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from . import AtomicMixin
from ..design_pattern.cart import AddCartCommand, RemoveCartCommand, GetCartCommand


class AddCartView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        command = AddCartCommand()
        data, status_code = command.execute(request)
        return Response(data=data, status=status_code)


class RemoveCartView(APIView, AtomicMixin):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        command = RemoveCartCommand()
        data, status_code = command.execute(request)
        return Response(data=data, status=status_code)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        command = GetCartCommand()
        data, status_code = command.execute(request)
        return Response(data=data, status=status_code)

