import pytest
from faker import Faker

from rest_framework.test import APIClient
from rest_framework.utils import json

from ..models import Admin
from product.models import Category, SubCategory


fake = Faker('fa_IR')


class SetUp:

    @pytest.fixture
    def set_up(self):
        self.admin = Admin.objects.create_superuser(username="admin", password="admin@123?")
        self.client = APIClient()
        payload = {"username": "admin", "password": "admin@123?"}
        response = self.client.post("/admins/login/", payload)
        self.access_token = json.loads(response.content).get("access")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)
        self.category = Category.objects.create(name='category')
        self.sub_category = SubCategory.objects.create(name='subcategory', category=self.category)


class TestViewAdmin(SetUp):

    @pytest.mark.django_db
    def test_admin_list(self, set_up):
        response = self.client.get(path='/admins/', content_type='application/json')
        assert response.status_code == 200
        for response in response.data:
            assert response['username'] == 'admin'

    @pytest.mark.django_db
    def test_admin_put(self, set_up):
        response = self.client.put(path=f'/admins/{self.admin.id}/', content_type='application/json')
        assert response.status_code == 200
        assert response.data['username'] == 'admin'

    @pytest.mark.django_db
    def test_admin_get(self, set_up):
        response = self.client.get(path=f'/admins/{self.admin.id}/', content_type='application/json')
        assert response.status_code == 200
        assert response.data['username'] == 'admin'

    @pytest.mark.django_db
    def test_admin_create(self, set_up):
        data = json.dumps({
            'username': 'sara',
            'first_name': 'sara',
            'last_name': 'nasiti',
            'phone_number': '09126939582',
            'email': 'sara@gmail.com',
            'password': '09126939581',
        })
        response = self.client.post(path='/admins/', data=data, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_admin_delete(self, set_up):
        response = self.client.delete(path=f'/admins/{self.admin.id}/', content_type='application/json')
        assert response.status_code == 204

    @pytest.mark.django_db
    def test_adminpermission_list(self, set_up):
        response = self.client.get(path='/admins/permissions/', content_type='application/json')
        assert response.status_code == 200
        assert response.data['id'] is not None
        assert response.data['admin_id'] is not None

    @pytest.mark.django_db
    def test_create_color(self, set_up):
        data = json.dumps({
            'code': '0000FF',
            'name': 'Blue',
        })
        response = self.client.post(path='/admins/color/', data=data, content_type='application/json')
        assert response.status_code == 201
        assert response.data['code'] == '0000FF'
        assert response.data['name'] == 'Blue'

    @pytest.mark.django_db
    def test_list_color(self, set_up):
        response = self.client.get(path='/admins/color/', content_type='application/json')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_create_category(self, set_up):
        data = json.dumps({
            'name': 'Category',
        })
        response = self.client.post(path='/admins/category/', data=data, content_type='application/json')
        assert response.status_code == 201
        assert response.data['name'] == 'Category'

    @pytest.mark.django_db
    def test_update_category(self, set_up):
        data = json.dumps({'name': 'test'})
        response = self.client.put(path=f'/admins/category/{self.category.id}/', data=data, content_type='application/json')
        assert response.status_code == 200
        assert response.data['name'] == 'test'
    #
    # @pytest.mark.django_db
    # def test_create_sub_category(self, set_up):
    #     data = json.dumps({
    #         'name': 'SubCategory',
    #         'category': self.category
    #     })
    #     print(data)
    #     response = self.client.post(path='/admins/sub-category/', data=data)
    #     assert response.status_code == 201
    #     assert response.data['name'] == 'SubCategory'

    @pytest.mark.django_db
    def test_update_sub_category(self, set_up):
        data = json.dumps({'name': 'test'})
        response = self.client.patch(path=f'/admins/sub-category/{self.sub_category.id}/', data=data, content_type='application/json')
        assert response.status_code == 200
        assert response.data['name'] == 'test'

