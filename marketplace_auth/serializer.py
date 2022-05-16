from rest_framework import serializers
from django.contrib.auth.models import User
# from marketplace.models import Buck
#
#
# class CategorySerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=50)
#     parent = serializers.CharField(max_length=50, allow_null=True, allow_blank=True)
#
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'parent']

class UserSerializer(serializers.Serializer):

    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

