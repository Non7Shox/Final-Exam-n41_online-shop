from django.urls import path
from products.views import ProductListView, ProductDetailView, ProductCreateView, UserProductListView, \
    ProductUpdateAPIView, ProductDeleteAPIView

app_name = 'users'

urlpatterns = [
    path('list/', ProductListView.as_view(), name='list'),
    path('myself/', UserProductListView.as_view(), name='myself'),
    path('<int:pk>/detail/', ProductDetailView.as_view(), name='detail'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('<int:pk>/update/', ProductUpdateAPIView.as_view(), name='update'),
    path('<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='delete'),
]
