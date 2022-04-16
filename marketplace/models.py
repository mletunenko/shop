import datetime
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


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
    categorys = models.ManyToManyField(Category, related_name='products')
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
