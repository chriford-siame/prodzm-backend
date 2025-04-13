from django.db import models
from prodzm.utils import product_image_upload_path
from django.db.models import Sum, F

class Category(models.Model):
    """
    Represents a product category (e.g., Electronics, Clothing) that groups similar products together.
    """
    name = models.CharField(max_length=255, help_text="The name of the category.")
    description = models.TextField(blank=True, help_text="Optional description of the category.")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents a product in the dropshipping store. 
    This model stores information about the product, its price, stockm and supplier.
    """
    name = models.CharField(max_length=255, help_text="The name of the product.")
    description = models.TextField(help_text="A detailed description of the product.")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product.")
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Shipping cost for this product.")
    remaining_stock = models.PositiveIntegerField(help_text="Remaining stock of this product.")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0, help_text="Product rating (from 0 to 5).")
    orders = models.PositiveIntegerField(default=0, help_text="Total number of orders made for this product.")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="Category to which this product belongs.")
    sku = models.CharField(max_length=255, unique=True, help_text="Unique Stock Keeping Unit (SKU) for this product.")
    supplier = models.CharField(max_length=255, help_text="Name of the product supplier.")
    
    def __str__(self):
        return self.name

    def is_available(self):
        """
        Returns whether the product is available based on remaining stock.
        """
        return self.remaining_stock > 0
    
    def get_all_images(self):
        """
        Returns a list of all images associated with the product, including the main image and additional images.
        """
        # Get the main image
        main_image = self.product_images

        # Get all additional images (excluding the main image)
        additional_images = self.images.exclude(is_main=True)

        # Combine the main image with the additional images into a list
        all_images = [main_image] + list(additional_images)

        return all_images
    
    def has_images(self):
        """
        Returns True if the current product has associated images otherwise returns False.
        """
        if self.images:
            return True
        return False
    
class ProductImage(models.Model):
    """
    Represents an image associated with a product. This can be the main image or additional images.
    """
    image = models.ImageField(upload_to=product_image_upload_path, help_text="Image file for the product.")
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE, help_text="Product associated with this image.")
    is_main = models.BooleanField(default=False, help_text="Whether this image is the main product image.")

    def __str__(self):
        return f"Image for {self.product.name} {'(Main)' if self.is_main else '(Additional)'}"

    def save(self, *args, **kwargs):
        """
        Ensure only one image is set as the main image for a product.
        """
        if self.is_main:
            # Set all other images for the product to not be the main image
            ProductImage.objects.filter(product=self.product).update(is_main=False)
        super().save(*args, **kwargs)

class Customer(models.Model):
    """
    Represents a customer who places orders on the website. This includes their contact information and shipping address.
    """
    first_name = models.CharField(max_length=255, help_text="Customer's first name.")
    last_name = models.CharField(max_length=255, help_text="Customer's last name.")
    email = models.EmailField(unique=True, help_text="Customer's email address (must be unique).")
    phone_number = models.CharField(max_length=15, blank=True, help_text="Customer's phone number (optional).")
    shipping_address = models.TextField(help_text="Customer's shipping address.")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class OrderItem(models.Model):
    """
    Represents an individual item in an order. Each item is linked to a product and order.
    """
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE, help_text="Order this item belongs to.")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, help_text="Product being ordered.")
    quantity = models.PositiveIntegerField(help_text="Quantity of the product being ordered.")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price of the product at the time of the order.")

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"

class Order(models.Model):
    """
    Represents an order placed by a customer, containing details about the status and total price.
    """
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, help_text="Customer who placed the order.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the order was created.")
    status = models.CharField(
        max_length=50, 
        choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], 
        default='pending', 
        help_text="Current status of the order."
    )
    total_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, help_text="Total price of the order.")

    def save(self, *args, **kwargs):
        # Calculate total price from related OrderItems
        if self.pk and self.items.exists():
            total = self.items.aggregate(
                total=Sum(F('unit_price') * F('quantity'))
            )['total'] or 0

            self.total_price = total
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} by {self.customer}"

class Shipping(models.Model):
    """
    Represents shipping information for an order, including tracking number and shipping status.
    """
    order = models.ForeignKey('Order', on_delete=models.CASCADE, help_text="Order associated with this shipping info.")
    tracking_number = models.CharField(max_length=255, help_text="Tracking number for the shipped order.")
    status = models.CharField(
        max_length=50, 
        choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('in_transit', 'In Transit'), ('delivered', 'Delivered')], 
        default='pending', 
        help_text="Current shipping status of the order."
    )
    shipped_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the order was shipped.")
    delivered_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the order was delivered.")

    def __str__(self):
        return f"Shipping for Order #{self.order.id}"

class Review(models.Model):
    """
    Represents a review left by a customer for a product they purchased.
    Includes rating and text feedback.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, help_text="Product being reviewed.")
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, help_text="Customer who left the review.")
    rating = models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], help_text="Rating given to the product.")
    comment = models.TextField(help_text="Text feedback or review provided by the customer.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time when the review was created.")

    def __str__(self):
        return f"Review for {self.product.name} by {self.customer.first_name}"
