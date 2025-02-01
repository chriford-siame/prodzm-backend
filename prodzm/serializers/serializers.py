from rest_framework import serializers
from prodzm.models import (
    Category,
    Product,
    ProductImage,
    Customer,
    Order,
    OrderItem,
    Shipping,
    Review,
)
from django.db.models.aggregates import Avg

class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.
    """
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'is_main')


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()  # Display category name
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'price', 'remaining_stock', 'orders', 'rating', 
            'average_rating', 'sku', 'images', 'is_available'
        )
        read_only_fields = ('sku', 'average_rating')

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj)
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return 0


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    """
    customer = serializers.StringRelatedField()  # Display customer name

    class Meta:
        model = Review
        fields = ('id', 'product', 'customer', 'rating', 'review_text', 'created_at')
        read_only_fields = ('created_at',)


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for Customer model.
    """
    class Meta:
        model = Customer
        fields = ('id', 'first_name', 'last_name', 'email', 'phone_number')


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'quantity', 'unit_price')
        read_only_fields = ('unit_price',)


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.
    """
    customer = CustomerSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.FloatField(source='get_total_price', read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'customer', 'status', 'created_at', 'updated_at', 'items', 'total_price')
        read_only_fields = ('created_at', 'updated_at', 'total_price')

    def get_total_price(self, obj):
        return sum([item.quantity * item.unit_price for item in obj.items.all()])


