import pytest

from django.forms.models import model_to_dict

from api.users.serializers import AccountSerializer
from api.users.models import Account

from .factories import AccountFactory


@pytest.mark.django_db
class TestAccountSerializer:
    def test_add_account(self, db):
        client = AccountFactory.build()
        serializer = AccountSerializer(data=model_to_dict(client))
        assert serializer.is_valid()
        serializer.save()
        assert Account.objects.filter(email=client.email).exists()

    def test_add_account_duplicate(self, db):
        account = AccountFactory()
        serializer = AccountSerializer(data=model_to_dict(account))
        assert not serializer.is_valid()
        assert "email" in serializer.errors.keys()

    def test_read_account(self, db):
        client = AccountFactory()
        serializer = AccountSerializer(client)
        assert {"pk", "email"} == set(serializer.data.keys())
