from rest_framework.routers import DefaultRouter

from prodzm.viewsets import (
    ProductViewSet, ProductImageViewSet, CategoryViewSet, ReviewViewSet,
    CustomerViewSet, OrderViewSet, OrderItemViewSet, ShippingViewSet, UserViewSet
)

# Create a router and register the ViewSets
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'reviews', ReviewViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'shipping', ShippingViewSet)

app_name = 'prodzm'
urlpatterns = router.urls
