from abc import ABC, abstractmethod

from django.db import transaction
from rest_framework import serializers

from applications.vending_machine.models import Product, Transaction
from applications.vending_machine.utils import amount_to_coins


class IProcessPayment(ABC):
    product: Product
    change: list[int]
    total_spent: int

    @abstractmethod
    def buy(self):
        raise NotImplementedError()


class ProcessPayment(IProcessPayment):
    _coins: list[int] = Transaction.coins.values

    def __init__(self, product, amount: int, user):
        self.product = product
        self.amount = amount
        self.user = user

        self.total_spent: int = product.cost * amount

    @transaction.atomic
    def buy(self):
        user_balance: int = self.user.get_balance()
        if user_balance < self.total_spent:
            raise serializers.ValidationError("Not enough money")
        self._do_transaction(self.total_spent)
        self.change = ChangeCoinService(self.total_spent, user_balance).change()
        self._do_transaction(sum(self.change))

    def _do_transaction(self, total_spent: int):
        self._fetch_product_amount()
        coins_to_withdraw = amount_to_coins(total_spent, self._coins)
        for coin in coins_to_withdraw:
            Transaction.objects.create(
                user=self.user,
                amount=coin,
                type=Transaction.transaction_type_choices.WITHDRAW,
            )

    def _fetch_product_amount(self):
        product = self.product
        if product.amount_available < self.amount:
            raise serializers.ValidationError("Not enough product available")
        product.amount_available -= self.amount
        product.save()


class ChangeCoinService:
    coins: list[int] = Transaction.coins.values

    def __init__(self, money_spent: int, user_balance: int):
        self.amount = user_balance - money_spent

    def change(self) -> list[int]:
        return amount_to_coins(self.amount, self.coins)
