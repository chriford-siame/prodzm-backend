from datetime import datetime
from django.utils.text import slugify
import os

def product_image_upload_path(instance, filename):
    """
    Generates the upload path for product images in the format: `product_name/YYYY-MM-DD/filename`
    - Uses a slugified version of the product name to ensure a clean file path.
    - Uses the current date in `YYYY-MM-DD` format.
    """
    date_str = datetime.now().strftime("%Y-%m-%d")  # Get current date
    product_name = slugify(instance.product.name)  # Slugify product name to remove spaces and special characters
    filename = slugify(os.path.splitext(filename)[0]) + os.path.splitext(filename)[1]  # Ensure clean filename
    
    return f"product_images/{product_name}/{date_str}/{filename}"
