import pytest

from ..viewsets import AdviceViewSet

from .factories import AdviceFactory


@pytest.fixture
def advice():
    return AdviceFactory()


@pytest.fixture
def advice_vs():
    return AdviceViewSet
