from django.core.exceptions import ValidationError


def multiple_of_5(value):
    if value % 5 != 0:
        raise ValidationError("Amount must be a multiple of 5")
