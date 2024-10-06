import pytest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase


User = get_user_model()


class RegisterViewTest(APITransactionTestCase):
    reset_sequences = True

    @pytest.mark.django_db
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_payload = {
            'title': 'Mr',
            'phone_number': '9034253647',
            'country_code': '1',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        self.invalid_payload = {
            'title': '',
            'phone_number': '1234567890',
            'country_code': '1',
            'first_name': '',
            'last_name': 'Doe'
        }

    def test_create_valid_user(self):
        response = self.client.post(self.register_url, self.valid_payload)
        # response.data => can see details of error
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().first_name, 'John')

    def test_create_invalid_user(self):
        response = self.client.post(self.register_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'error': {'title': ['This field may not be blank.'], 'phone_number': ['Enter a valid phone_number']}}
        )

