import uuid

from django.db import models

from applications.vending_machine.models.model_validations import multiple_of_5


class TransactionTypeChoices(models.IntegerChoices):
    DEPOSIT = 0, "Deposit"
    WITHDRAW = 1, "Withdraw"


class TransactionCoins(models.IntegerChoices):
    cent_5 = 5, "5 cents"
    cent_10 = 10, "10 cents"
    cent_20 = 20, "20 cents"
    cent_50 = 50, "50 cents"
    cent_100 = 100, "100 cents"


class Transaction(models.Model):
    coins = TransactionCoins
    transaction_type_choices = TransactionTypeChoices
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.PositiveIntegerField(validators=[multiple_of_5], choices=coins.choices)
    type = models.PositiveIntegerField(choices=transaction_type_choices.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to="authentication.User",
        on_delete=models.RESTRICT,
        related_name="transactions",
    )

    class Meta:
        verbose_name = "Deposit Transaction"
        verbose_name_plural = "Deposit Transactions"
        ordering = ["created_at"]

    @property
    def show_type(self) -> str:
        return dict(self.transaction_type_choices.choices)[self.type]

    @classmethod
    def reconstruct_state(cls, user_id: int) -> dict:
        transactions = cls.objects.filter(user_id=user_id).values("amount", "type")
        balance = 0
        for transaction in transactions:
            if transaction["type"] == TransactionTypeChoices.DEPOSIT.value:
                balance += transaction["amount"]
            else:
                balance -= transaction["amount"]
        return {'balance': balance}
