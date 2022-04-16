from rest_framework import serializers
from .models import Category, Product, Bucket, BucketProduct


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=50)
    parent = serializers.CharField(max_length=50, allow_null=True,
                                   allow_blank=True)

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


class BucketProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product_id')
    name = serializers.CharField(source='product.name')

    class Meta:
        model = BucketProduct
        fields = ['id', 'name', 'number']


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
