from rest_framework.routers import DefaultRouter

from applications.vending_machine.views.product import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
urlpatterns = router.urls
