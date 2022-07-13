from django_filters import rest_framework as filters

from applications.vending_machine.models import Product


class ProductFilter(filters.FilterSet):
    product_name = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = '__all__'
