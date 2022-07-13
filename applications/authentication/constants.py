from django.db import models


class GROUPS(models.TextChoices):
    ADMIN: str = "Admin"
    BUYER: str = "Buyer"
