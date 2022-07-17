import pytest
from faker import Faker

from rest_framework.test import APIClient

from ..models import User, Wallet, Token

fake = Faker('fa_IR')


class SetUp:

    @pytest.fixture
    def set_up(self):
        self.phone_number = '09' + fake.msisdn()[:9]
        self.phone_number_1 = '091' + fake.msisdn()[:8]
        self.client = APIClient()
        self.user = User.objects.create(phone_number=self.phone_number_1)


class TestViewLoginLogOut(SetUp):

    @pytest.mark.django_db
    def test_signup(self, set_up):
        response = self.client.post(path='/user/signup/', data={'phone_number':self.phone_number}, format='json')
        user = User.objects.get(phone_number=self.phone_number)
        assert Wallet.objects.get(user_id=user) is not None
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_login(self, set_up):
        response = self.client.post(path='/user/login/', data={'phone_number':self.phone_number_1}, format='json')
        assert response.status_code == 202
        assert response.data['phone_number'] == self.phone_number_1

    @pytest.mark.django_db
    def test_logout(self, set_up):
        self.user.is_authenticated = True
        self.user.save()
        self.access_token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.access_token)

        response = self.client.post(path='/user/logout/', format='json')
        assert response.status_code == 200

        user = User.objects.get(phone_number=self.phone_number_1)
        assert user.is_authenticated is False

