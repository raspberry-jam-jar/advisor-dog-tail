import pytest

from rest_framework.test import APIRequestFactory


@pytest.fixture
def request_factory():
    """
    Get an instance of DRF request factory.
    """
    return APIRequestFactory()
