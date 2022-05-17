from django.test import TestCase
import factory
from rest_framework.test import APITestCase
from factory.django import DjangoModelFactory
from factory import Faker, Sequence
from django.urls import reverse
from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker('last_name')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Sequence(lambda n: 'person{}@example.com'.format(n))
    password = Faker('last_name')


class AuthenticationTests(APITestCase):

    def test_post_registration(self):
        user = UserFactory()
        data = {
            "username": user.username + '_test',
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": user.password
        }
        response = self.client.post('/registration/', data=data)
        self.assertEqual(response.status_code, 201)

    def test_post_login(self):
        user = UserFactory()
        data = {
            "username": user.username,
            "password": user.password
        }
        response = self.client.post('/login/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_post_logout(self):
        user = UserFactory()
        self.client.force_login(user)
        response = self.client.post('/logout/')
        self.assertEqual(response.status_code, 200)
