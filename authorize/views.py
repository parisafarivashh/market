from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from twilio.rest import Client

from market import settings
from market.utils import generate_totp
from .models import User
from .serializers import RegisterSerializers, OtpSerializers


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializers
    queryset = User.objects.all()


class SendOtpView(generics.CreateAPIView):
    serializer_class = OtpSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        # we don`t need to save the data
        totp = generate_totp(request.data['phone_number'])
        # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send SMS
        # message = client.messages.create(
        #     body=f'Your OTP is: {totp}',
        #     from_=settings.TWILIO_PHONE_NUMBER,
        #     to=f'{request.data["country_code"]}{request.data["phone_number"]}'
        # )
        return Response(data={'totp':totp},  status=status.HTTP_201_CREATED)

