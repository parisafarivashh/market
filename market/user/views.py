from datetime import datetime

from rest_framework import status
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Token
from .permissions import IsUserProfile
from .serializers import UserPhoneNumberSerializer, WalletDetailSerializer, \
    UserProfileSerializer
from helpers import fa_to_eng_number
from exceptions import UserNotFound

from order.models import Order


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone_number = fa_to_eng_number(request.data.get('phone_number'))
        if not phone_number:
            data = {'detail': 'Please enter the your phone number'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise UserNotFound

        token = Token.objects.get(user=user)
        user.is_authenticated = True
        user.save()

        # Return the token + user data
        serializer = UserPhoneNumberSerializer(user)
        data = {'token': token.key}
        data.update(serializer.data)
        return Response(data=data, status=status.HTTP_202_ACCEPTED)


class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone_number = fa_to_eng_number(request.data.get('phone_number'))
        serializer = UserPhoneNumberSerializer(data={'phone_number': phone_number})
        serializer.is_valid(raise_exception=True)
        obj = serializer.validated_data
        try:
            # We already have authenticated user with this phone_number
            check_user = User.objects.get(phone_number=obj.get('phone_number'))
            data = {
                'detail': 'User already exist',
                'name': check_user.username
            }
            return Response(data=data, status=status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            user = User.objects.create(phone_number=obj.get('phone_number'))
            Order.objects.create(user=user)
            user.date_joined = datetime.now()
            user.save(update_fields=['date_joined'])
            return Response(data=obj, status=status.HTTP_200_OK)


class WalletDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletDetailSerializer

    def get_object(self):
        return self.request.user.wallet


class UserProfile(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsUserProfile]
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        user.is_authenticated = False
        user.save(update_fields=['is_authenticated'])
        return Response(status=status.HTTP_200_OK)

