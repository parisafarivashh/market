
import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from authorize.models import User
from core.models import Category


class CategoryViewTest(APITransactionTestCase):
    reset_sequences = True

    @pytest.mark.django_db
    def setUp(self):
        self.categories = reverse('list_create_category')

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

        self.valid_payload = {
            "title": "category",
            "parent": ''
        }

        self.category1 = Category(title='category 1')
        self.category1.save()
        self.category2 = Category(title='category 2', parent=self.category1)
        self.category2.save()


    def test_create_category(self):
        token = AccessToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.post(self.categories, self.valid_payload)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.json() == \
               {'id': 3,'title': 'category', 'parent': None, 'children': []}

    def test_list_category(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        response = self.client.get(self.categories)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert response.json() == \
               [
                   {
                       'children': [{
                           'children': [],
                           'id': 2,
                           'parent': 1,
                           'title': 'category 2'
                       }],
                       'id': 1,'parent': None, 'title': 'category 1'
                   }
               ]


