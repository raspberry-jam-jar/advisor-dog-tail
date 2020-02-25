import pytest

from .factories import UserFactory, AccountFactory

from api.users.viewsets import AccountViewset


@pytest.fixture
def account_vs():
    """
    Account viewset fixture.
    """
    return AccountViewset


@pytest.fixture
def user():
    """
    The factory for making a standard user model.
    """
    return UserFactory(is_staff=False, is_superuser=False)


@pytest.fixture
def manager():
    """
    The factory for making a manager user model.
    """
    return UserFactory(is_staff=True, is_superuser=False)


@pytest.fixture
def superuser():
    """
    The factory for making a superuser user model.
    """
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def bot():
    """
    The factory for making a standard user model for a bot.
    """
    return UserFactory(is_bot=True, is_staff=False, is_superuser=False)


@pytest.fixture
def bot_father():
    return UserFactory(is_bot=True, is_staff=True, is_superuser=True)


@pytest.fixture
def account():
    """
    The factory for making a standard account model.
    """
    return AccountFactory()
