from rest_framework import serializers

from applications.vending_machine.models import Product


def multiple_of_5(value):
    if value % 5 != 0:
        raise serializers.ValidationError("Amount must be a multiple of 5")


class ProductSerializer(serializers.ModelSerializer):
    cost = serializers.IntegerField(validators=[multiple_of_5])
    seller_full_name = serializers.CharField(source="seller.get_full_name", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        extra_kwargs = {'seller': {'write_only': True}}
