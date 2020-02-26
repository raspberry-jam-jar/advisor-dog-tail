import pytest

from . import factories
from ..models import Advice

# Create your tests here.


@pytest.mark.django_db
class TestAdviceModel:
    def test_create_model(self, db):
        advice = factories.AdviceFactory()
        assert Advice.objects.filter(slug=advice.slug).exists()
