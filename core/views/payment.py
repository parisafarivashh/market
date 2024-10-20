from rest_framework.views import APIView

from ..views import AtomicMixin


class PaymentView(APIView, AtomicMixin):

    def post(self, request, *args, **kwargs):
        pass
