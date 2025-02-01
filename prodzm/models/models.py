from django.db import models

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
    This model stores information about the product, its price, stock, supplier, and associated images.
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
    main_image = models.ForeignKey('ProductImage', related_name='main_product', on_delete=models.CASCADE, help_text="Main image for the product.")
    
    def __str__(self):
        return self.name

    def is_available(self):
        """
        Returns whether the product is available based on remaining stock.
        """
        return self.remaining_stock > 0

class ProductImage(models.Model):
    """
    Represents an image associated with a product. This can be the main image or additional images.
    """
    image = models.ImageField(upload_to='products/images/', help_text="Image file for the product.")
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

