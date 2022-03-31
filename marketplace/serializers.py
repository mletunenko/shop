from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    parent = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    description = serializers.CharField()
    category = serializers.CharField(source='category.name')


    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'category']
