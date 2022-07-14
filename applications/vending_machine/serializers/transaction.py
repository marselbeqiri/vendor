from rest_framework import serializers

from applications.vending_machine.models import Transaction
from applications.vending_machine.serializers.serializer_validations import multiple_of_5


class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.ChoiceField(validators=[multiple_of_5], choices=Transaction.coins)
    buyer_full_name = serializers.CharField(source="user.get_full_name", read_only=True)
    type_label = serializers.CharField(source="show_type", read_only=True)
    type = serializers.ChoiceField(choices=Transaction.transaction_type_choices.choices)

    class Meta:
        model = Transaction
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}


class DepositBalanceSerializer(serializers.Serializer):
    balance = serializers.IntegerField()
