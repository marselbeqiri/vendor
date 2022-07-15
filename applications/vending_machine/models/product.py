import uuid

from django.db import models, transaction

from applications.common.models import Track
from applications.vending_machine.models.model_validations import multiple_of_5

__all__ = [
    "Product",
]


class ProductAudit(Track):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount_available = models.PositiveIntegerField()
    product = models.ForeignKey(
        to="vending_machine.Product",
        on_delete=models.CASCADE,
        related_name="audits",
    )

    class Meta:
        verbose_name = "Product Audit"
        verbose_name_plural = "Product Audits"
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"P {self.product_id} - {self.product.product_name}"

    def save(self, *args, **kwargs):
        return None if self.id else super().save(*args, **kwargs)


class Product(Track):
    product_name = models.CharField(max_length=100)
    amount_available = models.PositiveIntegerField()
    cost = models.PositiveIntegerField(validators=[multiple_of_5])
    seller = models.ForeignKey(
        to="authentication.User",
        on_delete=models.RESTRICT,
        related_name="products",
    )
    audit_log = ProductAudit

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.product_name}"

    @transaction.atomic
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.audit_log = ProductAudit.objects.create(
            amount_available=self.amount_available,
            product=self,
        )
