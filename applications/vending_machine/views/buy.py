from abc import ABC, abstractmethod

from django.db import transaction
from rest_framework import mixins, status
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.vending_machine.models import Product, Transaction
from applications.vending_machine.services.buy import IProcessPayment, ProcessPayment
from applications.vending_machine.utils import amount_to_coins


class BuyProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    amount = serializers.IntegerField()


class BuyResponseSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.product_name')
    amount = serializers.IntegerField()
    total_spent = serializers.IntegerField()
    # change = serializers.IntegerField(many=True, read_only=True)
    change = serializers.ListField(
        child=serializers.IntegerField(min_value=0, max_value=100)
    )


class BuyViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    Deposit is constructed by using event sourcing technique.
    So it will contain only creation of a new transaction events (Deposit/Withdraw).
    State of the deposit is reconstructed from the events amount (Sum,Sub Deposits and Withdraws).
    """
    serializer_class = BuyProductSerializer
    response_serializer_class = BuyResponseSerializer

    # permission_classes = [TransactionPermission]
    queryset = Product.objects.all().select_related('seller')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return self.perform_create(serializer)

    @transaction.atomic
    def perform_create(self, serializer):
        validated_data = serializer.validated_data
        product = get_object_or_404(Product, id=validated_data['product_id'])
        buy_service: IProcessPayment = ProcessPayment(product=product,
                                                      amount=validated_data['amount'],
                                                      user=self.request.user)
        buy_service.buy()
        response = self.response_serializer_class(buy_service)

        return Response(response.data, status=status.HTTP_201_CREATED)
