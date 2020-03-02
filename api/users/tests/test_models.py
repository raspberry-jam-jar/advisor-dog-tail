import pytest

from django.contrib.auth import get_user_model

from api.users.models import Account

from .factories import UserFactory, AccountFactory


@pytest.mark.django_db
class TestUserModel:
    User = get_user_model()

    def test_making_user(self, db):
        user = UserFactory(is_active=True)
        does_exist = self.User.objects.filter(email=user.email, is_active=True).exists()
        assert does_exist

    def test_making_admin(self, db):
        admin = UserFactory(is_active=True, is_staff=True, is_superuser=True)
        does_exist = self.User.objects.filter(
            email=admin.email, is_active=True, is_staff=True, is_superuser=True
        ).exists()
        assert does_exist


@pytest.mark.django_db
class TestAccountModel:
    def test_making_client(self, db):
        account = AccountFactory()
        assert Account.objects.filter(email=account.email).exists()
