from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.urls', namespace='users')),
    path('api/v1/products/', include('products.urls', namespace='products')),
    path('api/v1/cart/', include('cartandorders.urls', namespace='cartandorders')),
]
