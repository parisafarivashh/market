from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from authorize.utils import generate_totp, validate_totp
from .filters import FilterUser
from .models import User
from .serializers import RegisterSerializers, UserListSerializers, \
    PhoneSerializer, OtpSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializers
    queryset = User.objects.all()


class SendOtpView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = PhoneSerializer

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
    serializer_class = OtpSerializer

    @action(detail=False, methods=['post'])
    @transaction.atomic()
    def bind(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        validate_totp(
            phone=request.data['phone_number'],
            code=request.data['otp_code']
        )

        user = get_object_or_404(
            User,
            phone_number=request.data['phone_number'],
            country_code=request.data['country_code'],
        )
        user.is_verify = True
        user.save(update_fields=['is_verify'])
        return Response(data='', status=status.HTTP_201_CREATED)


class LoginView(generics.CreateAPIView):
    serializer_class = OtpSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = get_object_or_404(
                User,
                phone_number=request.data['phone_number'],
                country_code=request.data['country_code'],
            )
        except Http404:
            raise Http404({'data': 'Invalid login data.'})

        validate_totp(
            phone=request.data['phone_number'],
            code=request.data['otp_code'],
        )

        token = AccessToken.for_user(user)
        return Response(data={'access': str(token)}, status=status.HTTP_200_OK)


class ListUserView(mixins.ListModelMixin, GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = UserListSerializers
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = {
    #     "title": ["icontains", "exact"], # worked on modelviewsets
    #     "first_name": ["icontains"],
    #     "last_name": ["icontains"],
    #     "phone_number": ["exact"],
    #     "is_staff": ["exact"],
    # }
    filterset_class = FilterUser

    def get_queryset(self):
        return User.objects.filter(~Q(id=self.request.user.id))

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

