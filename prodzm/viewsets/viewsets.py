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
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.db.models import Q
from prodzm.serializers import (
    ProductSerializer, 
    ProductImageSerializer, 
    CategorySerializer, 
    ReviewSerializer,
    CustomerSerializer, 
    OrderSerializer, 
    OrderItemSerializer, 
    ShippingSerializer,
    UserSerializer,
)
from django.contrib.auth.models import User

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Custom API endpoint to filter products by category.\n
        Example: /api/products/search/?category=Electronics
        """
        queryset = Product.objects.all()
        
        # Filtering by category (if provided)
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__name=category)

        # Filtering by number of orders (if provided)
        orders = request.query_params.get('orders')
        if orders and orders != 0:
            queryset = queryset.filter(orders__gte=orders)

        # Filtering by creation date (if provided)
        date = request.query_params.get('date')
        if date:
            queryset = queryset.filter(created_at__date=date)

        # Filtering by price range (if provided)
        price = request.query_params.get('price')
        if price and price != 0:
            queryset = queryset.filter(price__lte=price)

        # Search query across multiple fields
        qs = request.query_params.get('qs')
        if qs:
            queryset = queryset.filter(
                Q(name__icontains=qs) | Q(description__icontains=qs)
            )

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product images.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product categories.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        lookup_value = self.kwargs.get(self.lookup_field)
        
        # Try ID lookup first
        if lookup_value.isdigit():
            try:
                return User.objects.get(id=lookup_value)
            except User.DoesNotExist:
                raise NotFound("User with this ID does not exist.")
        
        # Fallback to username lookup
        try:
            return User.objects.get(username=lookup_value)
        except User.DoesNotExist:
            raise NotFound("User with this username does not exist.")

    lookup_field = 'lookup'  # Custom URL parameter
    
class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing product reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customers.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can manage customers

class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing order items.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShippingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing shipping details.
    """
    queryset = Shipping.objects.all()
    serializer_class = ShippingSerializer
    permission_classes = [permissions.IsAuthenticated]
