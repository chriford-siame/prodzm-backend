from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
from .models import OrderItem, Order

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    Recalculate and update the total price of the order
    whenever an OrderItem is added, updated, or deleted.
    """
    order = instance.order

    if order.items.exists():
        total = order.items.aggregate(
            total=Sum(F('unit_price') * F('quantity'))
        )['total'] or 0
        order.total_price = total
    else:
        order.total_price = 0

    order.save()
