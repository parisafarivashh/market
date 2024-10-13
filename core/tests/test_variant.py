import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from authorize.models import User
from core.models import Category, Product, Variant


class VariantViewTest(APITransactionTestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.variant = reverse('create_list_variant')

        self.user = User.objects.create_user(
            title='userr',
            phone_number='9024356728',
            country_code='98',
            password='password',
        )
        self.admin = User.objects.create_superuser(
            title='admin',
            phone_number='9034356728',
            country_code='98',
            password='password',
        )
        self.category = Category.objects.create(title="clothes")

        self.product = Product.objects.create(
            creator=self.user,
            title="T-shirt",
            category=self.category
        )

        self.valid_payload = {
            "number": 10,
            "price": 1300,
            "color": "blue",
            "material": "linen",
            "product": self.product.id,
        }

        self.variant1 = Variant.objects.create(
            number=10,
            price=1300,
            color="blue",
            material="linen",
            product=self.product,
        )

        self.variant2 = Variant.objects.create(
            number=20,
            price=1200,
            color="yellow",
            material="linen",
            product=self.product,
        )


    def test_create_variant(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.post(self.variant, self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.json() is not None
        assert response.json()["number"] == 10
        assert response.json()["price"] == 1300.0
        assert response.json()["material"] == 'linen'
        assert response.json()["product"] is not None

    def test_list_variant(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.get(self.variant)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.json()) == 2
        for response in response.json():
            assert len(response) == 6

    def test_update_variant(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.patch(f'{self.variant}/{self.variant1.id}', {'number': 2})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.json()['number'] == 2

    def test_removed_variant(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.delete(f'{self.variant}/{self.variant1.id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        assert response.json() == \
               {
                   'error':
                       {'detail': [
                           'You do not have permission to perform this action.'
                       ]}
               }

        token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        response = self.client.delete(f'{self.variant}/{self.variant1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

