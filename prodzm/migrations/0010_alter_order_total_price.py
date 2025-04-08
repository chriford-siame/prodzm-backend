# Generated by Django 5.1.5 on 2025-04-08 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("prodzm", "0009_remove_product_product_images"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="total_price",
            field=models.DecimalField(
                decimal_places=2,
                help_text="Total price of the order.",
                max_digits=10,
                null=True,
            ),
        ),
    ]
