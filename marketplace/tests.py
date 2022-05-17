# TODO test deletion permissions Category and Product
# TODO test available items product field


import factory
from factory.django import DjangoModelFactory
from factory import Faker, Sequence
from django.urls import reverse

from rest_framework.test import APITestCase
from django.utils import timezone

from marketplace.models import Category, Product
from django.contrib.auth.models import User



class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = 'test_category'
    parent = None


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('last_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Sequence(lambda n: 'person{}@example.com'.format(n))


class StaffUserFactory(UserFactory):
    is_staff = True


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = Faker('first_name')
    price = 100
    description = 'Some short description'
    available_items = Faker().unique.random_int()


class SaleFactory(DjangoModelFactory):
    name = Faker('first_name')
    announcement_date = factory.LazyFunction(timezone.now() - timezone.timedelta(days=1))
    start_date = factory.LazyFunction(timezone.now() - timezone.timedelta(minutes=1))
    end_date = factory.LazyFunction(timezone.now() + timezone.timedelta(days=1))
    was_announced = False
    discount = 15


class CategoryViewSetTests(APITestCase):
    def test_get_category_list_unauthorized_user(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_category_list_unauthorized_user(self):
        data = {
            'name': 'test_category',
            'parent': ''
        }
        response = self.client.post(reverse('category-list'), data=data)
        self.assertEqual(response.status_code, 403)

    def test_get_category_list_authorized_user(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_category_list_authorized_user(self):
        user = UserFactory()
        self.client.force_login(user)
        data = {
            'name': 'test_category',
            'parent': ''
        }
        response = self.client.post(reverse('category-list'), data=data)
        self.assertEqual(response.status_code, 403)

    def test_get_category_list_staff_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_category_list_staff_user_no_parent(self):
        data = {
            'name': 'test_category',
            'parent': ''
        }
        user = StaffUserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('category-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_category_list_staff_user_with_parent(self):
        parent_category = CategoryFactory()
        data = {
            'name': 'test_category',
            'parent': parent_category.id
        }
        user = StaffUserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('category-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_get_category_detail_unauthorized_user(self):
        """
        category {id} tests
        """
        category = CategoryFactory()
        response = self.client.get(reverse('category-detail', args=(category.id,)))
        self.assertEqual(response.status_code, 200)

    def test_get_category_detail_authorized_user(self):
        user = UserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        response = self.client.get(reverse('category-detail', args=(category.id,)))
        self.assertEqual(response.status_code, 200)

    def test_get_category_detail_staff_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        response = self.client.get(reverse('category-detail', args=(category.id,)))
        self.assertEqual(response.status_code, 200)

    def test_put_category_detail_unauthorized_user(self):
        category = CategoryFactory()
        data = {
            "name": "New test category",
            "parent": ''
        }
        response = self.client.put(reverse('category-detail', args=(category.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_category_detail_authorized_user(self):
        user = UserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        data = {
            "name": "New test category",
            "parent": ''
        }
        response = self.client.put(reverse('category-detail', args=(category.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_category_detail_staff_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        data = {
            "name": "New test category",
            "parent": ''
        }
        response = self.client.put(reverse('category-detail', args=(category.id,)), data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_category_detail_staff_user_partial(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        parent = CategoryFactory()
        category = CategoryFactory()
        data = {
            "parent": [parent.id]
        }
        response = self.client.put(reverse('category-detail', args=(category.id,)), data=data)
        self.assertEqual(response.status_code, 400)

    def test_patch_category_detail_unauthorized_user(self):
        category = CategoryFactory()
        data = {
            "name": "New test"
        }
        response = self.client.patch(reverse('category-detail', args=(category.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_patch_category_detail_authorized_user(self):
        user = UserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        data = {
            "name": "New test"
        }
        response = self.client.put(reverse('category-detail', args=(category.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_patch_category_detail_staff_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        parent = CategoryFactory()
        category = CategoryFactory()
        data = {
            "parent": [parent.id]
        }
        response = self.client.patch(reverse('category-detail', args=(category.id,)), data=data)
        self.assertEqual(response.status_code, 200)


class ProductViewSetTests(APITestCase):
    def test_get_product_list_unauthorized_user(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_product_list_authorized_user(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_product_list_unauthorized_user(self):
        data = {
            "name": "product",
            "price": 100,
            "description": "short description"
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 403)

    def test_post_product_list_authorized_user(self):
        user = UserFactory()
        self.client.force_login(user)
        data = {
            "name": "product",
            "price": 100,
            "description": "short description"
        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 403)

    def test_post_product_list_staff_user(self):
        user = StaffUserFactory()
        category = CategoryFactory()
        self.client.force_login(user)
        data = {
            "name": "product",
            "price": 100,
            "description": "short description",
            'categories': [
                category.id
            ]

        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_product_list_negative_price(self):
        user = StaffUserFactory()
        category = CategoryFactory()
        self.client.force_login(user)
        data = {
            "name": "product",
            "price": -100,
            "description": "short description",
            'categories': [
                category.id
            ]

        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_product_list_partial(self):
        user = StaffUserFactory()
        category = CategoryFactory()
        self.client.force_login(user)
        data = {
            "name": "product",
            "price": 100,
            "description": "short description",
            "available_items": 13

        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_post_product_list_decimal_places(self):
        user = StaffUserFactory()
        category = CategoryFactory()
        self.client.force_login(user)
        data = {
            "name": "product",
            "price": 23.1233,
            "description": "short description",
            "available_items": 13,
            'categories': [
                category.id
            ]

        }
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_get_product_detail_unauth_user(self):
        product = ProductFactory()
        response = self.client.get(reverse('product-detail', args=(product.id,)))
        self.assertEqual(response.status_code, 200)

    def test_get_product_detail_auth_user(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        response = self.client.get(reverse('product-detail', args=(product.id,)))
        self.assertEqual(response.status_code, 200)

    def test_get_product_detail_staff_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        response = self.client.get(reverse('product-detail', args=(product.id,)))
        self.assertEqual(response.status_code, 200)

    def test_put_product_detail_unauth_user(self):
        product = ProductFactory()
        data = {}
        response = self.client.put(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_product_detail_auth_user(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        data = {}
        response = self.client.put(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_put_product_detail_staff_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        product = ProductFactory()
        product.categories.add(category)
        data = {
            'name': "New name",
            'price': product.price,
            'description': product.description,
            "available_items": 13,
            'category': product.categories
        }
        response = self.client.put(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 200)

    def test_put_product_detail_staff_user_partial(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        product = ProductFactory()
        product.categories.add(category)
        data = {
            'name': "New name",
            'category': product.categories
        }
        response = self.client.put(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 400)

    def test_patch_product_detail_unauth_user(self):
        category = CategoryFactory()
        product = ProductFactory()
        product.categories.add(category)
        data = {
            'name': "New name",
            'category': product.categories
        }
        response = self.client.patch(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_patch_product_detail_unauth_user(self):
        user = UserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        product = ProductFactory()
        product.categories.add(category)
        data = {
            'name': "New name",
            'category': product.categories,
            "available_items": 13
        }
        response = self.client.patch(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 403)

    def test_patch_product_detail_staff_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        product = ProductFactory()
        product.categories.add(category)
        data = {
            'name': "New name",
            'category': product.categories
        }
        response = self.client.patch(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 200)

    def test_patch_product_detail_staff_user_negative_price(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        category = CategoryFactory()
        product = ProductFactory()
        product.categories.add(category)
        data = {
            'price': -10
        }
        response = self.client.patch(reverse('product-detail', args=(product.id,)), data=data)
        self.assertEqual(response.status_code, 400)

    def test_delete_product_detail_unauth_user(self):
        product = ProductFactory()
        response = self.client.patch(reverse('product-detail', args=(product.id,)))
        self.assertEqual(response.status_code, 403)

    def test_delete_product_detail_auth_user(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        response = self.client.patch(reverse('product-detail', args=(product.id,)))
        self.assertEqual(response.status_code, 403)

    def test_delete_product_detail_auth_user(self):
        user = StaffUserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        response = self.client.patch(reverse('product-detail', args=(product.id,)))
        self.assertEqual(response.status_code, 200)


class BucketViewSetTests(APITestCase):
    bucket_url = '/bucket/'
    bucket_add_url = '/bucket/add'

    def test_get_bucket_unauth_user(self):
        response = self.client.get(self.bucket_url)
        self.assertEqual(response.status_code, 403)

    def test_get_bucket_auth_user(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.get(self.bucket_url)
        self.assertEqual(response.status_code, 200)

    def test_post_bucket_add_auth_user(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        data = {
            "id": product.id,
            "number": 2
        }
        response = self.client.post(self.bucket_add_url, data)
        self.assertEqual(response.status_code, 200)

    def test_post_bucket_add_auth_user_negavite_amount(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        data = {
            "id": product.id,
            "number": -2
        }
        response = self.client.post(self.bucket_add_url, data)
        self.assertEqual(response.status_code, 400)

    def test_post_bucket_add_double(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        data = {
            "id": product.id,
            "number": 2
        }
        self.client.post(self.bucket_add_url, data)
        response = self.client.post(self.bucket_add_url, data)
        self.assertEqual(response.status_code, 400)

    def test_put_bucket_update_negavite_amount(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        data = {
            "id": product.id,
            "number": 2
        }
        self.client.post(self.bucket_add_url, data)
        data = {
            "number": -3
        }
        response = self.client.put(f'/bucket/{product.id}/update', data)
        self.assertEqual(response.status_code, 400)

    def test_delete_bucket_product(self):
        user = UserFactory()
        self.client.force_login(user)
        product = ProductFactory()
        data = {
            "id": product.id,
            "number": 2
        }
        self.client.post(self.bucket_add_url, data)
        response = self.client.delete(f'/bucket/{product.id}')
        self.assertEqual(response.status_code, 200)



