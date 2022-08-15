import pytest
from faker import Faker

from rest_framework.test import APIClient
from rest_framework.utils import json

from user.models import User, Token

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


# class TestViewProduct(SetUp):

    # @pytest.mark.django_db
    # def test_product_create(self, set_up):
    #     data = json.dumps({
    #         "name": "product",
    #         "sub_category": "1",
    #         "details": [{"color": "1", "size": "1", "price": "200000", "count": "1"}]
    #     })
    #     response = self.client.post(path='/product/create/',
    #                                 data=json.loads(data),
    #                                 content_type='application/json')
    #     assert response.status_code == 200

    # @pytest.mark.django_db
    # def test_product_list(self, set_up):
    #     response = self.client.get(path='/product/', content_type='application/json')
    #     print(response.data)
    #     assert response.status_code == 200

