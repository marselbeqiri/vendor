from typing import Any

from django.contrib.auth import password_validation
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from applications.authentication.constants import GROUPS


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    def create_user(self, username: str, password: str, **extra_fields):
        """
        Create and save a user with the given data.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if email := extra_fields.pop("email", ''):
            email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        self.validate_password(password, user)
        user.set_password(password)
        user.save()
        # self.put_on_admin_group(user)

        return user

    @staticmethod
    def validate_password(password: str, user=None):
        password_validation.validate_password(password, user)

    def create_superuser(self, username: str, password: str = None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    @staticmethod
    def put_on_admin_group(user: Any) -> Group:
        group_name = GROUPS.ADMIN
        group, is_created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        user.save()

        return group
