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
from django.contrib.auth.models import User
from django.db.models.aggregates import Avg
import json
class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for ProductImage model.
    """
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'is_main')


class RelatedProductSerializer(serializers.ModelSerializer):
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
            'average_rating', 'sku', 'images', 'is_available', 'has_images',
        )
        read_only_fields = ('sku', 'average_rating')

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj)
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return 0

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    """
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()  # Display category name
    average_rating = serializers.FloatField(source='get_average_rating', read_only=True)
    related_products = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'price', 'remaining_stock', 'orders', 'rating', 
            'average_rating', 'sku', 'images', 'is_available', 'has_images', 'related_products'
        )
        read_only_fields = ('sku', 'average_rating')

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj)
        if reviews.exists():
            return reviews.aggregate(Avg('rating'))['rating__avg']
        return 0
    
    def get_related_products(self, obj):
        """Fetch other products in the same category (excluding current product)"""
        related = Product.objects.filter(category=obj.category).exclude(id=obj.id)
        return RelatedProductSerializer(related, many=True).data


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for Review model.
    """
    customer = serializers.StringRelatedField()  # Display customer name

    class Meta:
        model = Review
        fields = ('id', 'product', 'customer', 'rating', 'comment', 'created_at')
        read_only_fields = ('created_at',)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """

    class Meta:
        model = User
        fields = '__all__'


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
        fields = ('id', 'customer', 'status', 'created_at', 'items', 'total_price')
        read_only_fields = ('created_at', 'total_price')

    def get_total_price(self, obj):
        return sum([item.quantity * item.unit_price for item in obj.items.all()])


class ShippingSerializer(serializers.ModelSerializer):
    """
    Serializer for Shipping model.
    """
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Shipping
        fields = ('id', 'order', 'tracking_number', 'status', 'shipped_at', 'delivered_at')
        read_only_fields = ('shipped_at', 'delivered_at')

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """
    class Meta:
        model = Category
        fields = ('id', 'name', 'description')