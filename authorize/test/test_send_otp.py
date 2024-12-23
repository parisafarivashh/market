import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from authorize.models import User


class SendOtpViewTest(APITransactionTestCase):
    reset_sequences = True

    @pytest.mark.django_db
    def setUp(self):
        self.send_otp = reverse('send_otp')
        self.user = User(
            title='user',
            phone_number='9024356728',
            country_code='98',
            password='password',
        )
        self.user.save()

        self.valid_payload = {
            'phone_number': '9034253647',
            'country_code': '98',
        }
        self.invalid_payload = {
            'phone_number': '1234567890',
            'country_code': '1',
        }

    def test_send_otp(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.post(self.send_otp, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert 'totp' in response.data
        otp = response.data['totp']
        assert len(otp) == 4
        assert otp.isdigit()

    def test_send_otp_invalid_user(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.post(self.send_otp, self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'error': {'phone_number': ['Enter a valid value.']}}
        )

