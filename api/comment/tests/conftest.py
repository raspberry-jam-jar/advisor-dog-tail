import pytest

from api.advice.tests.conftest import advice  # noqa: F401
from api.users.tests.conftest import django_user  # noqa: F401

from ..viewsets import CommentViewSet
from .factories import CommentFactory


@pytest.fixture
def comment():
    return CommentFactory()


@pytest.fixture
def comment_vs():
    return CommentViewSet
