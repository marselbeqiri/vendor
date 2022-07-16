from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.db import transaction

from applications.authentication.constants import GROUPS


class Command(BaseCommand):
    help = 'Create Init Data'
    default_password = 'Vending!123'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        seller_group, buyer_group = self.create_groups()
        user_model = get_user_model()

        if not user_model.objects.filter(username='admin').exists():
            admin = user_model.objects.create_superuser(
                username='admin',
                password=self.default_password,
                first_name='Admin',
                last_name='Admin'
            )
            admin.groups.add(seller_group.id)
            admin.groups.add(buyer_group.id)
            admin.save()

        if not user_model.objects.filter(username='buyer').exists():
            buyer = user_model.objects.create_user(
                username='buyer',
                password=self.default_password,
                first_name='Buyer',
                last_name='One'
            )
            buyer.groups.add(buyer_group.id)
            buyer.save()

        if not user_model.objects.filter(username='seller').exists():
            seller = user_model.objects.create_user(
                username='seller',
                password=self.default_password,
                first_name='Seller',
                last_name='One'
            )
            seller.groups.add(seller_group.id)

    def create_groups(self):
        admin = Group.objects.get_or_create(name=GROUPS.ADMIN)[0]
        buyer = Group.objects.get_or_create(name=GROUPS.BUYER)[0]
        return admin, buyer
