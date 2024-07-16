from rest_framework import serializers

from products.models import ProductModel
from users.models import UserModel


class ProductSearchSerializer(serializers.Serializer):
    q = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['uuid', 'avatar', 'username']


class ProductsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = ['id', 'name', 'description', 'photo', 'price', 'total', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']
