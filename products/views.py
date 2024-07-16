from django.db.models import Q
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.pagination import CustomPagination
from .models import ProductModel
from products.serializers import ProductsSerializer
from products.permissions import IsOwner


class ProductListView(generics.ListAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        query_param = self.request.query_params.get('q', None)
        order_param = self.request.query_params.get('order', 'created_at')
        name_startswith = self.request.query_params.get('name_startswith', None)
        name_order = self.request.query_params.get('name_order', None)

        queryset = ProductModel.objects.all()

        if query_param:
            queryset = queryset.filter(Q(name__icontains=query_param))

        if name_startswith:
            queryset = queryset.filter(Q(name__istartswith=name_startswith))

        if order_param in ['price', '-price', 'created_at', '-created_at']:
            queryset = queryset.order_by(order_param)

        if name_order == 'asc':
            queryset = queryset.order_by('name')
        elif name_order == 'desc':
            queryset = queryset.order_by('-name')

        return queryset


class UserProductListView(generics.ListAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return ProductModel.objects.filter(user=self.request.user)


class ProductDetailView(generics.RetrieveAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductUpdateAPIView(APIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        post = ProductModel.objects.filter(pk=pk)
        if not post.exists():
            response = {
                "status": True,
                "message": "Post does not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductsSerializer(post.first(), data=request.data, context={'request': request})
        if serializer.is_valid():
            self.check_object_permissions(obj=post.first(), request=request)
            serializer.save()
            response = {
                "status": True,
                "message": "Successfully updated"

            }
            return Response(response, status=status.HTTP_202_ACCEPTED)
        else:
            response = {
                "status": True,
                "message": "Invalid request",
                "errors": serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, pk):
        post = ProductModel.objects.filter(pk=pk)
        if not post.first():
            response = {
                "status": False,
                "message": "Post does not found"
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(post.first(), request)
        post.delete()
        response = {
            "status": True,
            "message": "Successfully deleted"

        }
        return Response(response, status=status.HTTP_202_ACCEPTED)
