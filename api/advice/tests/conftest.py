import pytest

from api.users.tests.conftest import django_user  # noqa: F401

from ..viewsets import AdviceViewSet
from ..models.tag import TagType, Tag

from .factories import AdviceFactory, TagFactory


@pytest.fixture
def advice():
    return AdviceFactory()


@pytest.fixture
def advice_vs():
    return AdviceViewSet


@pytest.fixture
def user_tag():
    return TagFactory()


@pytest.fixture
def default_tag():
    return Tag.objects.default()


@pytest.fixture
def default_tag_type():
    return TagType.objects.default()
