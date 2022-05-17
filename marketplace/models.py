import datetime
from django.contrib import admin
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('self', models.DO_NOTHING, null=True,
                               blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    available_items = models.IntegerField(validators=[MinValueValidator(limit_value=0)])
    categories = models.ManyToManyField(Category)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Bucket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='BucketProduct')

    def __str__(self):
        return f'Bucket of {self.user}'


class BucketProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    bucket = models.ForeignKey(Bucket, on_delete=models.CASCADE)
    number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'bucket')


class Sale(models.Model):
    name = models.CharField(max_length=100)
    announcement_date = models.DateTimeField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    was_announced = models.BooleanField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    products = models.ManyToManyField(Product, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    users = models.ManyToManyField(User, blank=True)
    groups = models.ManyToManyField(Group, blank=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product, through='OrderProduct')


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sale = models.ForeignKey(Sale, blank=True, on_delete=models.CASCADE)
    price_with_discount = models.DecimalField(max_digits=8, decimal_places=2)
    number = models.IntegerField()
