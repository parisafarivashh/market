from django.db import transaction
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from market.utils import generate_totp, validate_totp
from .models import User
from .serializers import RegisterSerializers, OtpSerializers, BindSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializers
    queryset = User.objects.all()


class SendOtpView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
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


class VerifyPhoneView(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BindSerializer

    @action(detail=False, methods=['post'])
    @transaction.atomic()
    def bind(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        is_valid = validate_totp(
            phone=request.data['phone_number'],
            code=request.data['otp_code']
        )
        if not is_valid:
            raise ValidationError(detail={'otp_code': 'Otp Code Is Not Valid'})

        user = get_object_or_404(
            User,
            phone_number=request.data['phone_number'],
            country_code=request.data['country_code'],
        )
        user.is_verify = True
        user.save(update_fields=['is_verify'])
        return Response(data='', status=status.HTTP_201_CREATED)

