from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from authorize.models import User


class VerifyPhoneNumberViewTest(APITransactionTestCase):
    reset_sequences = True

    @pytest.mark.django_db
    def setUp(self):
        self.verify_phone = reverse('verify_phone-bind')

        self.user = User(
            title='user',
            phone_number='9024356728',
            country_code='98',
            password='password',
        )
        self.user.save()

        self.valid_payload = {
            'phone_number': self.user.phone_number,
            'country_code': self.user.country_code,
            'otp_code': '2034',
        }
        self.invalid_payload = {
            'phone_number': '9034256756',
            'country_code': '1',
            'otp_code': '2333'
        }

    def test_bind_phone(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        with patch('authorize.views.validate_totp') as mock_verify_service:
            mock_verify_service.return_value = True

            response = self.client.post(self.verify_phone, self.valid_payload)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            user = get_object_or_404(User, id=self.user.id)
            assert user.is_verify is True

    def test_bind_phone_with_wrong_code(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.post(self.verify_phone, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'error': {'otp_code': ['Otp Code Is Not Valid']}}
        )
