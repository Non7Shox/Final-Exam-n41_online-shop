from django.contrib import admin
from .models import Cart, CartItem, OrderModel


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    list_filter = ('created_at', 'updated_at')


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'created_at', 'updated_at')
    search_fields = ('cart__user__username', 'product__name')
    list_filter = ('created_at', 'updated_at')


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone_number', 'address', 'status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone_number', 'address')
    list_filter = ('status', 'created_at', 'updated_at')
    ordering = ('-created_at',)
