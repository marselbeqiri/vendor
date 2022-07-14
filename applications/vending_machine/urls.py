from rest_framework.routers import DefaultRouter

from applications.vending_machine.views.deposit import DepositViewSet
from applications.vending_machine.views.product import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('deposit', DepositViewSet, basename='deposit')
urlpatterns = router.urls
