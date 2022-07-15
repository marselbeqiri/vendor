from rest_framework import serializers


class BuyProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class BuyResponseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.product_name')
    total_spent = serializers.IntegerField()
    change = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100)
    )
