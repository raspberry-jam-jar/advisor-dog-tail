import pytest

from ..models.advice import Advice
from ..models.tag import Tag

from . import factories

# Create your tests here.


@pytest.mark.django_db
class TestAdviceModel:
    def test_create_advice(self, db):
        advice = factories.AdviceFactory()
        assert Advice.objects.filter(slug=advice.slug).exists()

    def test_create_advice_with_default_tag(self, db, default_tag):
        from ..receivers import add_default_tag  # noqa: F401

        advice = factories.AdviceFactory()
        assert advice.tags.count() == 1
        assert advice.tags.first().slug == default_tag.slug


@pytest.mark.django_db
class TestTagModel:
    def test_create_tag(self, db):
        tag = factories.TagFactory()
        assert Tag.objects.filter(slug=tag.slug).exists()

    def test_create_tag_with_default_type(self, db, default_tag_type, user_tag):
        """Tag instance must be created with a default type (prochee)"""
        assert user_tag.type == default_tag_type
