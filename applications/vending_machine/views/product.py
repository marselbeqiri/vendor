from rest_framework.viewsets import ModelViewSet

from applications.vending_machine.filters import ProductFilter
from applications.vending_machine.models import Product
from applications.vending_machine.permissions import ProductPermission
from applications.vending_machine.serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().select_related('seller')
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    permission_classes = [ProductPermission]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def perform_update(self, serializer):
        serializer.save(seller=self.request.user)
