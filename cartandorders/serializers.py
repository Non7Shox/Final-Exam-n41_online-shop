from rest_framework import serializers

from cartandorders.models import OrderModel
from .models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']


class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        fields = ['phone_number', 'address']


class CheckoutSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)

    def validate_cart_id(self, value):
        try:
            cart = Cart.objects.get(id=value)
        except Cart.DoesNotExist:
            raise serializers.ValidationError(f"Cart with id {value} does not exist.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        cart_id = validated_data['cart_id']
        phone_number = validated_data['phone_number']
        address = validated_data['address']

        cart = Cart.objects.get(id=cart_id)

        order = OrderModel.objects.create(
            user=user,
            phone_number=phone_number,
            address=address,
            cart=cart
        )

        return order
