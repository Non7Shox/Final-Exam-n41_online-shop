from django.urls import path
from .views import CartAddView, CartListAPIView, CartDeleteView, CheckoutAPIView

app_name = 'carts'
urlpatterns = [
    path('add/', CartAddView.as_view(), name='add-to-cart'),
    path('all/', CartListAPIView.as_view(), name='cart-list'),
    path('remove/<int:pk>/', CartDeleteView.as_view(), name='cart-remove'),

    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),

]
