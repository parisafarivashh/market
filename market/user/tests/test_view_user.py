import pytest
from faker import Faker

from rest_framework.test import APIClient
from rest_framework.utils import json

from ..models import User, Wallet, Token

fake = Faker('fa_IR')


class SetUp:

    @pytest.fixture
    def set_up(self):
        self.phone_number = '09' + fake.msisdn()[:9]
        self.client = APIClient()
        self.user = User.objects.create(phone_number=self.phone_number)
        self.user.is_authenticated = True
        self.user.save()
        self.access_token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)


class TestViewUser(SetUp):

    @pytest.mark.django_db
    def test_detailWallet(self, set_up):
        response = self.client.get(path='/user/wallet', content_type='application/json')
        assert response.status_code == 200
        assert len(response.data) == 3

    @pytest.mark.django_db
    def test_profile_update(self, set_up):
        data = json.dumps({'username': 'sara'})
        response = self.client.patch(path='/user/profile', data=data, content_type='application/json')
        assert response.status_code == 200
        assert response.data['username'] == 'sara'

    @pytest.mark.django_db
    def test_profile_get(self, set_up):
        response = self.client.get(path='/user/profile', content_type='application/json')
        assert response.status_code == 200
        assert len(response.data) == 5

