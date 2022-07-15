from django.contrib.auth.models import Group
from faker import Faker
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse

from applications.authentication.constants import GROUPS
from applications.common.tests import BaseAPITestCase
from applications.vending_machine.models import Transaction


class TestBuyProductAPIViews(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('buy-list')
        cls.faker = Faker()
        cls.product_payload = dict(
            product_name=cls.faker.first_name(),
            amount_available=cls.faker.random_int(min=1, max=30),
            cost=25,
        )

    def setUp(self):
        self.product = baker.make('vending_machine.Product', **self.product_payload, _fill_optional=True)
        self.buy_payload = dict(
            product_id=self.product.id,
            amount=5,
        )

    def create_buyer_and_authorize(self):
        self.authorize_client()
        self.set_buyer_role()

    def set_seller_role(self):
        group, is_created = Group.objects.get_or_create(name=GROUPS.ADMIN)
        self.user.groups.add(group)

    def set_buyer_role(self):
        group, is_created = Group.objects.get_or_create(name=GROUPS.BUYER)
        self.user.groups.add(group)

    def test__buy_product_401_unauthorized(self):
        response = self.client.post(self.url, self.buy_payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test__buy_product_403_forbidden(self):
        self.authorize_client()
        response = self.client.post(self.url, self.buy_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test__insufficient_funds(self):
        self.create_buyer_and_authorize()
        response = self.client.post(self.url, self.buy_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], "Not enough money")

    def test__only_buyers_are_allowed_403(self):
        self.authorize_client()
        self.set_seller_role()
        response = self.client.post(self.url, self.buy_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test__buy_product_and_deposit(self):
        self.create_buyer_and_authorize()
        deposit_coins = [100, 50, 20]
        for i in deposit_coins:
            self.add_funds(i)
        deposit_balance = self.get_balance()
        self.assertEqual(deposit_balance, sum(deposit_coins))

        response = self.client.post(self.url, self.buy_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['total_spent'], self.product.cost * self.buy_payload['amount'])
        self.assertEqual(sum(response.data['change']), sum(deposit_coins) - response.data['total_spent'])

    def add_funds(self, amount: int):
        url = reverse('deposit-list')
        payload = dict(amount=amount, type=Transaction.transaction_type_choices.DEPOSIT)
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def get_balance(self):
        return self.user.get_balance()
