from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from utils.pagination import CustomPagination
from .models import Cart, CartItem, OrderModel
from .serializers import CartItemSerializer, CartAddSerializer, CartSerializer, \
    CheckoutSerializer
from products.models import ProductModel


class CartAddView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CartAddSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            cart, created = Cart.objects.get_or_create(user=request.user)

            product = get_object_or_404(ProductModel, pk=product_id)

            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            serializer = CartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartListAPIView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = CustomPagination




class CartDeleteView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            product = ProductModel.objects.get(pk=pk)
        except ProductModel.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.delete()
            return Response({"message": "Product removed from cart."}, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)
        except CartItem.DoesNotExist:
            return Response({"error": "Product not in cart."}, status=status.HTTP_404_NOT_FOUND)


class CheckoutAPIView(generics.CreateAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = CheckoutSerializer

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            cart_id = serializer.validated_data.get('cart_id')
            phone_number = serializer.validated_data.get('phone_number')
            address = serializer.validated_data.get('address')

            try:
                cart = Cart.objects.get(id=cart_id)
            except Cart.DoesNotExist:
                return Response({"detail": f"Cart with id {cart_id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

            order = OrderModel.objects.create(
                user=request.user,
                phone_number=phone_number,
                address=address,
                cart=cart
            )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
