from django.contrib.auth.models import AbstractUser
from django.db import models

from applications.authentication.constants import GROUPS
from applications.authentication.models.user_manager import UserManager


class User(AbstractUser):
    email = models.EmailField(blank=True)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]
    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.get_full_name()

    def is_seller(self) -> bool:
        return self.groups.filter(name=GROUPS.ADMIN).exists()

    def is_buyer(self) -> bool:
        return self.groups.filter(name=GROUPS.BUYER).exists()

    def can_buy(self, money_spent: int) -> bool:
        balance = self.get_balance()
        return self.is_buyer() and balance >= money_spent

    def get_balance(self) -> int:
        transaction_model = self.transactions.model
        return transaction_model.reconstruct_state(self.id)["balance"]
