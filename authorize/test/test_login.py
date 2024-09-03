from unittest.mock import patch

import pytest
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken
from twilio.jwt import access_token

from authorize.models import User


class LoginViewTest(APITransactionTestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.login = reverse('login')

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

    def test_login(self):
        with patch('authorize.views.validate_totp') as mock_verify_service:
            mock_verify_service.return_value = True

            response = self.client.post(self.login, self.valid_payload)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            assert response.data['access'] is not None

    def test_login_wrong_number(self):
        response = self.client.post(self.login, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data,
            {'error': {'data': ['Invalid login data.']}}
        )

