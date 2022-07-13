from django.core.exceptions import ValidationError
from django.db import models

from applications.common.models import Track

__all__ = [
    "Product",
]


def multiple_of_5(value):
    if value % 5 != 0:
        raise ValidationError("Amount must be a multiple of 5")


class Product(Track):
    product_name = models.CharField(max_length=100)
    amount_available = models.PositiveIntegerField()
    cost = models.PositiveIntegerField(validators=[multiple_of_5])
    seller = models.ForeignKey(
        to="authentication.User",
        on_delete=models.RESTRICT,
        related_name="products",
    )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.product_name}"
