from django.contrib import admin
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

class ProductImageInline(admin.TabularInline):
    """
    Allows product images to be managed directly within the Product admin panel.
    Uses a TabularInline layout for a compact display.
    """
    model = ProductImage
    extra = 1  # Allows adding one additional image inline by default
    fields = ('image', 'is_main')
    ordering = ['-is_main']  # Show the main image first


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing products in the admin panel.
    """
    list_display = ('name', 'category', 'price', 'remaining_stock', 'orders', 'rating', 'is_available')
    list_filter = ('category', 'rating', 'remaining_stock')
    search_fields = ('name', 'sku', 'supplier')
    prepopulated_fields = {"sku": ("name",)}  # Auto-generate SKU from name
    ordering = ('-orders', 'name')  # Sort by most ordered products first
    inlines = [ProductImageInline]  # Show related images within the product admin panel

    def is_available(self, obj):
        return obj.remaining_stock > 0
    is_available.boolean = True  # Show a checkmark (✔) in the admin panel


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing product images.
    """
    list_display = ('product', 'image', 'is_main')
    list_filter = ('is_main',)
    search_fields = ('product__name',)
    ordering = ['product', '-is_main']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing product categories.
    """
    list_display = ('name', 'description')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin configuration for managing customer reviews.
    """
    list_display = ('product', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'customer__first_name', 'customer__last_name')
    ordering = ('-created_at',)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    Admin configuration for Customer model.
    """
    list_display = ('first_name', 'last_name', 'email', 'phone_number')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')


class OrderItemInline(admin.TabularInline):
    """
    Inline admin configuration for Order Items within the Order admin view.
    """
    model = OrderItem
    extra = 1
    fields = ('product', 'quantity', 'unit_price')
    readonly_fields = ('unit_price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin configuration for Order model.
    """
    list_display = ('id', 'customer', 'created_at', 'status', 'total_price')
    list_filter = ('status', 'created_at')
    search_fields = ('customer__first_name', 'customer__last_name', 'id')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for OrderItem model.
    """
    list_display = ('order', 'product', 'quantity', 'unit_price')
    search_fields = ('product__name', 'order__id')
    ordering = ('order',)


@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    """
    Admin configuration for Shipping model.
    """
    list_display = ('order', 'tracking_number', 'status', 'shipped_at', 'delivered_at')
    list_filter = ('status', 'shipped_at', 'delivered_at')
    search_fields = ('tracking_number', 'order__id')
    ordering = ('-shipped_at',)
