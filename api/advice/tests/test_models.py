import pytest

from model_bakery import baker

from ..receivers import add_default_tag
from ..models import Advice, Tag

from . import factories

# Create your tests here.


@pytest.mark.django_db
class TestAdviceModel:
    def test_create_model(self, db, the_other_tag):
        advice = factories.AdviceFactory()
        assert Advice.objects.filter(slug=advice.slug).exists()

    def test_create_model_with_default_tag(self, db, the_other_tag):
        """
        Advice instance must be created with a default tag (прочее)
        using the connected signal handler 
        """
        advice = factories.AdviceFactory()
        assert advice.tags.count() == 1
        assert advice.tags.first().slug == the_other_tag.slug


@pytest.mark.django_db
class TestTagModel:
    def test_create_model(self, db):
        tag = factories.TagFactory()
        assert Tag.objects.filter(slug=tag.slug).exists()
