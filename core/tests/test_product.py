import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from authorize.models import User
from core.models import Product, Category


class ProductViewTest(APITransactionTestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.products = reverse('list_create_product')

        self.user = User(
            title='user',
            phone_number='9024356728',
            country_code='98',
            password='password',
        )
        self.user.save()

        self.admin = User.objects.create_superuser(
            title='admin',
            phone_number='9034356728',
            country_code='98',
            password='password',
        )

        self.category1 = Category(title='category 1')
        self.category1.save()

        self.valid_payload = {
            "category": self.category1.id,
            "title": "T-shirt",
            "variants":[{"number": 10, "price":2300, "color": "fff", "material":"nakh" }],
            "attributes":[{"title":"height", "value": "short"}]
        }

        self.product1 = Product.objects.create(title='Product1', category=self.category1, creator=self.user)
        self.product2 = Product.objects.create(title='Product2', category=self.category1, creator=self.user)

    def test_create_product(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.post(self.products, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.json()["attributes"] is not None
        assert response.json()["variants"] is not None
        assert response.json()["id"] is not None

    def test_list_product(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.get(self.products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.json()) == 2
        for response in response.json():
            assert len(response) == 7

    def test_get_product(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        response = self.client.get(f'{self.products}/{self.product1.id}')
        assert len(response.json()) == 7
        assert response.json()["category"] is not None
        assert response.json()["attributes"] == []
        assert response.json()["variants"] == []

    def test_delete_product(self):
        token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        response = self.client.delete(f'{self.products}/{self.product1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

