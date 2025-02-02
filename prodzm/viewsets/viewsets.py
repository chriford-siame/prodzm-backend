from rest_framework import viewsets, permissions
from prodzm.models import (
    Product, 
    ProductImage, 
    Category, 
    Review, 
    Customer, 
    Order, 
    OrderItem, 
    Shipping
)
from prodzm.serializers import (
    ProductSerializer, 
    ProductImageSerializer, 
    CategorySerializer, 
    ReviewSerializer,
    CustomerSerializer, 
    OrderSerializer, 
    OrderItemSerializer, 
    ShippingSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

