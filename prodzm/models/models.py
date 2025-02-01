from django.db import models

class Category(models.Model):
    """
    Represents a product category (e.g., Electronics, Clothing) that groups similar products together.
    """
    name = models.CharField(max_length=255, help_text="The name of the category.")
    description = models.TextField(blank=True, help_text="Optional description of the category.")

    def __str__(self):
        return self.name

