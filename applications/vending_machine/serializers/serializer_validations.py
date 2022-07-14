from rest_framework import serializers


def multiple_of_5(value):
    if value % 5 != 0:
        raise serializers.ValidationError("Amount must be a multiple of 5")
