from django.contrib.auth.models import Group
from faker import Faker
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse

from applications.authentication.constants import GROUPS
from applications.common.tests import BaseAPITestCase


class TestProductListCreateAPIViews(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('product-list')
        cls.faker = Faker()
        cls.create_payload = dict(
            product_name=cls.faker.first_name(),
            amount_available=cls.faker.random_int(min=1, max=30),
            cost=25,
        )

    def setUp(self):
        self.authorize_client()

    def set_seller_role(self):
        group, is_created = Group.objects.get_or_create(name=GROUPS.ADMIN)
        self.user.groups.add(group)

    def test__product_create_403(self):
        response = self.client.post(self.url, self.create_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test__product_list_create(self):
        self.set_seller_role()

        baker.make('vending_machine.Product', _quantity=5, _fill_optional=True)
        response = self.client.post(self.url, self.create_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 6)


class TestProductRetrieveUpdateDestroyAPIViews(BaseAPITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('product-detail', args=[1])
        cls.faker = Faker()
        cls.create_payload = dict(
            product_name=cls.faker.first_name(),
            amount_available=cls.faker.random_int(min=1, max=30),
            cost=25,
        )

    def setUp(self):
        self.authorize_client()
        self.set_seller_role()
        self.product = baker.make('vending_machine.Product', seller=self.user, **self.create_payload)

    def set_seller_role(self):
        group, is_created = Group.objects.get_or_create(name=GROUPS.ADMIN)
        self.user.groups.add(group)

    def create_new_user(self):
        self.authorize_client()
        self.set_seller_role()

    def test__product_retrieve(self):
        self.set_seller_role()
        baker.make('vending_machine.Product', _quantity=5, _fill_optional=True)
        response = self.client.get(reverse('product-detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], self.create_payload['product_name'])

    def test__product_update(self):
        self.set_seller_role()
        baker.make('vending_machine.Product', _quantity=5, _fill_optional=True)
        response = self.client.put(self.url, self.create_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['product_name'], self.create_payload['product_name'])

    def test__should_update_product_only_seller_who_created(self):
        self.create_new_user()
        response = self.client.put(self.url, self.create_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test__product_delete(self):
        self.set_seller_role()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test__product_delete_403(self):
        self.create_new_user()
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
