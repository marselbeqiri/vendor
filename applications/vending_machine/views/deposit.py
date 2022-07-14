from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from applications.vending_machine.models import Transaction
from applications.vending_machine.permissions import TransactionPermission
from applications.vending_machine.serializers import TransactionSerializer
from applications.vending_machine.serializers.transaction import DepositBalanceSerializer


class DepositViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    Deposit is constructed by using event sourcing technique.
    So it will contain only creation of a new transaction events (Deposit/Withdraw).
    State of the deposit is reconstructed from the events amount (Sum,Sub Deposits and Withdraws).
    """
    serializer_class = TransactionSerializer

    permission_classes = [TransactionPermission]

    @swagger_auto_schema(
        method='get',
        responses={200: DepositBalanceSerializer()},
    )
    @action(detail=False, methods=['get'], name='Get deposit state', )
    def state(self, request):
        user = request.user
        state = Transaction.reconstruct_state(user_id=user.id)
        serializer = self.get_serializer(state)

        return Response(serializer.data)

    @swagger_auto_schema(
        method='get',
        responses={200: DepositBalanceSerializer()},
    )
    @action(detail=False, methods=['get'], name='Withdraw all deposit coins', url_path='reset')
    def reset(self, request):
        user_id = request.user.id
        balance = Transaction.reconstruct_state(user_id=user_id)['balance']
        if balance == 0:
            return Response(data={'balance': balance})
        payload = {
            'amount': balance,
            'type': Transaction.transaction_type_choices.WITHDRAW.value,
        }
        Transaction.objects.create(**payload, user_id=user_id)
        state = Transaction.reconstruct_state(user_id=user_id)
        serializer = self.get_serializer(state)

        return Response(serializer.data)

    def perform_create(self, serializer):
        balance = Transaction.reconstruct_state(user_id=self.request.user.id)['balance']
        if balance < serializer.validated_data['amount']:
            raise serializers.ValidationError('Insufficient balance')
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        return Transaction.objects.all().select_related('user').filter(user_id=self.request.user.id)

    def get_serializer_class(self):
        if self.action in ['state', 'reset']:
            return DepositBalanceSerializer
        return super().get_serializer_class()
