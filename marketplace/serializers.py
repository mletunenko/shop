from rest_framework import serializers
from .models import Category, Product, Bucket, BucketProduct, Sale


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'name', 'discount']

    def validate_discount(self, discount):
        if discount > 100 or discount < 0:
            raise serializers.ValidationError('discount must be from 0 to 100')
        return discount



class ProductSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    best_sale = SaleSerializer(required=False)
    price_with_discount = serializers.DecimalField(required=False, max_digits=8, decimal_places=2)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'categories',
                  'price_with_discount', 'best_sale']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price must be grater than 0')
        return price


class ProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'categories']

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Price must be grater than 0')
        return price


class BucketProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product_id')
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=8,
                                     decimal_places=2)
    best_sale = SaleSerializer(source='product.best_sale')
    price_with_discount = serializers.DecimalField(source='product.price_with_discount', max_digits=8, decimal_places=2)

    class Meta:
        model = BucketProduct
        fields = ['id', 'name', 'number', 'price', 'best_sale', 'price_with_discount']


class BucketProductAddSerializer(serializers.ModelSerializer):
    number = serializers.IntegerField()
    bucket_id = serializers.IntegerField()
    product_id = serializers.IntegerField()

    def create(self, validated_data):
        return BucketProduct.objects.create(**validated_data)

    def validate_product_id(self, product_id):
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError(
                f"No product id={product_id} in catalog")
        return product_id

    def validate_number(self, number):
        if number < 1:
            raise serializers.ValidationError("Number is less then one")
        elif number > 100:
            raise serializers.ValidationError("Number is more then 100")
        return number

    class Meta:
        model = BucketProduct
        fields = ['number', 'bucket_id', 'product_id']


class BucketProductUpdateProduct(serializers.ModelSerializer):
    number = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.number = validated_data.get('number', instance.number)
        instance.save()
        return instance

    class Meta:
        model = BucketProduct
        fields = ['number']
