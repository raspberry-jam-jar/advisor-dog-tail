import pytest

from .factories import UserFactory


@pytest.fixture
def django_user():
    """
    The factory for making a standard user model.
    """
    return UserFactory(is_staff=False, is_superuser=False)
