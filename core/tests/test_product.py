import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from authorize.models import User
from core.models import Product, Category


class ProductViewTest(APITransactionTestCase):
    reset_sequences = True  # Resets the auto-increment sequences at the start of each test

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
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.json() == {
            'id': 3,
            'title': 'T-shirt',
            'creator': 1,
            'category': 1,
            'attributes': [
                {'id': 1, 'title': 'height', 'value': 'short','product': 3}
            ],
            'variants': [
                {'number': 10, 'price': '2300.00', 'color': 'fff', 'material': 'nakh', 'product': 3}
            ]
        }

    def test_list_product(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.get(self.products)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.json() ==  [
            {
                'title': 'Product1',
                'id': 1,
                'creator': 1,
                'creator_title': 'user',
                'category': {'id': 1, 'title': 'category 1', 'parent': None, 'children': []},
                'attributes': [],
                'variants': []
            },
            {
                'id': 2,
                'title': 'Product2',
                 'creator': 1,
                 'creator_title': 'user',
                 'category': {'id': 1, 'title': 'category 1', 'parent': None, 'children': []},
                 'attributes': [], 'variants': []
             }
        ]

    def test_get_product(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        response = self.client.get(f'{self.products}/{self.product1.id}')
        assert response.json() ==  {
            'id': 1,
            'title': 'Product1',
            'category': {'id': 1, 'title': 'category 1', 'parent': None, 'children': []},
            'creator': 1,
            'creator_title': 'user',
            'attributes': [],
            'variants': []
        }

    def test_delete_product(self):
        token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        response = self.client.delete(f'{self.products}/{self.product1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




