from rest_framework import serializers

from applications.vending_machine.models import Product
from applications.vending_machine.serializers.serializer_validations import multiple_of_5


class ProductSerializer(serializers.ModelSerializer):
    cost = serializers.IntegerField(validators=[multiple_of_5])
    seller_full_name = serializers.CharField(source="seller.get_full_name", read_only=True)

    class Meta:
        model = Product
        exclude = ["seller"]
