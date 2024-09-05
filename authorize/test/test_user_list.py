import pytest
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase

from authorize.models import User
from authorize.serializers import UserListSerializers


class UserListTest(APITransactionTestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.list_user = reverse('list_user')

        self.admin = User.objects.create_superuser(
            title='user',
            phone_number='9024356728',
            country_code='98',
            password='password',
        )
        self.admin.save()
        self.token = Token.objects.create(user=self.admin)

        self.user2 = User(
            title='second',
            phone_number='9024356722',
            country_code='98',
            password='password',
        )
        self.user2.save()

        self.user3 = User(
            title='third',
            phone_number='9024356721',
            country_code='98',
            password='password',
        )
        self.user3.save()


    def test_list_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

        response = self.client.get(self.list_user, query_params=dict(title='third'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 1
        assert response.data[0] == UserListSerializers(instance=self.user3).data

        response = self.client.get(self.list_user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.data) == 2

