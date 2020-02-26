import pytest

from api.users.tests.conftest import django_user  # noqa: F401

from ..viewsets import AdviceViewSet

from .factories import AdviceFactory


@pytest.fixture
def advice():
    return AdviceFactory()


@pytest.fixture
def advice_vs():
    return AdviceViewSet
