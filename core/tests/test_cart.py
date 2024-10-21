from datetime import datetime

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITransactionTestCase
from rest_framework_simplejwt.tokens import AccessToken

from authorize.models import User
from core.models import Category, Variant, Product, Cart, CartItem


class CartViewTest(APITransactionTestCase):
    reset_sequences = True

    @pytest.mark.django_db
    def setUp(self):
        self.add_variant_in_cart = reverse('add_variant_in_cart')
        self.update_item_in_cart = reverse('update_item_in_cart')
        self.remove_item_in_cart = reverse('remove_item_in_cart')
        self.get_cart = reverse('list_cart')

        self.user = User(
            title='user',
            phone_number='9024356728',
            country_code='98',
            password='password',
        )
        self.user.save()

        self.user2 = User(
            title='user2',
            phone_number='9024356724',
            country_code='98',
            password='password',
        )
        self.user2.save()

        self.category = Category.objects.create(title='Clothes')
        self.product = Product.objects.create(
            creator=self.user,
            title='T-shirt',
            category=self.category,
        )
        self.variant = Variant.objects.create(
            number=10,
            price=1200,
            color='blue',
            material='catan',
            product=self.product,
        )

        self.cart = Cart.objects.create(
            user=self.user2,
            status='open',
            order_date=datetime.today().date()
        )

        self.cart_item = CartItem.objects.create(
            product=self.product,
            variant=self.variant,
            price=self.variant.price,
            quantity=3,
            cart=self.cart
        )


    def test_add_variant_in_cart(self):
        token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        payload_add_variant = {"variant": self.variant.id}
        response = \
            self.client.post(self.add_variant_in_cart, payload_add_variant)

        assert Cart.objects.filter(user=self.user).count() == 1
        assert Cart.objects.filter(user=self.user).values_list('status', flat=True).first() == 'open'
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        assert response.json() == \
               {
                   'cart':
                       {
                           'id': 2,
                           'payable_amount': 1200,
                           'item_count': 1,
                           'status': 'open',
                           'order_date': None
                       },
                   'cart_items': [
                       {
                           'id': 2,
                           'cart_id': 2,
                           'price': 1200,
                           'product': {
                               'id': 1,
                               'title': 'T-shirt',
                               'category': {
                                   'id': 1,
                                   'title': 'Clothes',
                                   'parent': None,
                                   'children': []
                               }
                           },
                           'variant': {
                               'id': 1,
                               'number': 10,
                               'price': '1200.00',
                               'color': 'blue',
                               'material': 'catan'
                           },
                           'quantity': 1}
                   ]
               }


    def test_update_item_in_cart(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        payload_update_quantity = {
            "cart_item_id": self.cart_item.id,
            "cart_id": self.cart.id,
            "quantity": 2,
        }
        response = \
            self.client.patch(self.update_item_in_cart, payload_update_quantity)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert CartItem.objects.filter(id=self.cart_item.id) \
                   .values_list('quantity', flat=True).first() == 2


    def test_get_cart(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')
        response = self.client.get(self.get_cart)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        assert len(response.json()) == 2
        assert 'cart' in response.json()
        assert 'cart_items' in response.json()
        assert len(response.json()['cart']) == 5

    def test_remove_item_from_cart(self):
        token = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(token)}')

        payload_remove_item = {
            "cart_item_id": self.cart_item.id,
            "cart_id": self.cart.id,
        }
        response = self.client.delete(self.remove_item_in_cart, payload_remove_item)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        assert self.cart.cartItems.count() == 0

