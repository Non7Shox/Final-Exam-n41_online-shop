from django.contrib import admin
from .models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'price', 'total', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'price', 'total')
    search_fields = ('name', 'description', 'user__username')
    ordering = ('-created_at',)
