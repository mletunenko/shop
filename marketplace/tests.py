import datetime
import os

import factory
from factory.django import DjangoModelFactory
from factory import Faker, Sequence
from django.urls import reverse

from django.test import TestCase
from django.utils import timezone

from marketplace.models import Category, Product, Bucket, BucketProduct, Sale
from django.contrib.auth.models import User
import marketplace.views


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = 'test_category'
    parent = None


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        # database = 'shop'

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


class SaleFactory(DjangoModelFactory):
    name = Faker('first_name')
    announcement_date = factory.LazyFunction(timezone.now() - timezone.timedelta(days=1))
    start_date = factory.LazyFunction(timezone.now() - timezone.timedelta(minutes=1))
    end_date = factory.LazyFunction(timezone.now() + timezone.timedelta(days=1))
    was_announced = False
    discount = 15


class ProductViewSetTests(TestCase):

    def test_get_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, 200)

    def test_normal_product(self):
        test_category = CategoryFactory()
        data = {
            'name': 'test_product1',
            'price': 100,
            'description': 'short description',
            'categories': [
                test_category.id
            ]
        }
        user = StaffUserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 201)

    def test_negative_price_product(self):
        test_category = CategoryFactory()
        data = {
            'name': 'test_product3',
            'price': -100,
            'description': 'short description',
            'categories': [
                test_category.id
            ]
        }
        user = StaffUserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 400)

    def test_forbiden_user(self):
        test_category = CategoryFactory()
        data = {
            'name': 'test_product3',
            'price': 100,
            'description': 'short description',
            'categories': [
                test_category.id
            ]
        }
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post(reverse('product-list'), data=data)
        self.assertEqual(response.status_code, 403)

class CategoryViewSetTests(TestCase):
    def test_get_category_list_unaythorized_user(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)

    def test_post_category_list_unaythorized_user(self):
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



