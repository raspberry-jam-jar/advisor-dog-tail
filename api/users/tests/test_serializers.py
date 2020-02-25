import pytest

from django.forms.models import model_to_dict

from api.users.serializers import AccountSerializer, ReadOnlyAccountSerializer
from api.users.models import Account

from .factories import AccountFactory


@pytest.mark.django_db
class TestClientSerializer:
    def test_add_client(self, db):
        client = AccountFactory.build()
        serializer = AccountSerializer(data=model_to_dict(client))
        assert serializer.is_valid()
        model = serializer.create(serializer.validated_data)
        assert Account.objects.filter(email=model.email).exists()

    def test_add_client_duplicate(self, db):
        account = AccountFactory()
        serializer = AccountSerializer(data=model_to_dict(account))
        assert not serializer.is_valid()
        assert "email" in serializer.errors.keys()

    def test_read_client(self, db):
        client = AccountFactory()
        serializer = ReadOnlyAccountSerializer(client)
        assert {"pk", "email"} == set(serializer.data.keys())
