import pytest

from django.forms.models import model_to_dict

from ..serializers import AdviceSerializer, TagSerializer
from ..receivers import add_default_tag  # noqa: F401
from ..models import Advice, Tag

from .factories import AdviceFactory, TagFactory


# Create your tests here.
@pytest.mark.django_db
class TestAdviceSerializer:
    def test_create_advice(self, db):
        advice = AdviceFactory.build()
        serializer = AdviceSerializer(data=model_to_dict(advice))
        serializer.is_valid(raise_exception=True)
        model = serializer.save()
        assert Advice.objects.filter(slug=model.slug).exists()

    def test_update_advice(self, subtests, db):
        advice = AdviceFactory()
        new_advice = AdviceFactory.build()
        assert not Advice.objects.filter(title=new_advice.title).exists()
        serializer = AdviceSerializer(
            advice, data={"title": new_advice.title, "link": new_advice.link}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert Advice.objects.filter(
            title=new_advice.title, link=new_advice.link
        ).exists()

    def test_partial_update_advice(self, subtests, db):
        new_advice = AdviceFactory.build()
        for field in ("title", "link"):
            with subtests.test(msg=f"test_edit_{field}"):
                advice = AdviceFactory()
                value = getattr(new_advice, field)
                serializer = AdviceSerializer(advice, data={field: value}, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                assert Advice.objects.filter(**{field: value}).exists()

        # Editing slug field should be forbidden
        with subtests.test(msg="test_edit_slug"):
            advice = AdviceFactory()
            serializer = AdviceSerializer(
                advice, data={"slug": new_advice.slug}, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            assert not Advice.objects.filter(
                title=advice.title, slug=new_advice.slug
            ).exists()

    def test_update_advice_tags_using_ru(self, db, the_other_tag):
        """
        Update existing advice with a new set of tags
        """
        advice = AdviceFactory()
        tags = [{"title": "видео"}, {"title": "аудио"}, {"title": "текст"}]
        serializer = AdviceSerializer(advice, data={"tags": tags}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        lookup_tag_data = list(map(lambda t: t["title"], tags))
        assert Advice.objects.filter(tags__title__in=lookup_tag_data).exists()
        assert advice.tags.filter(title__in=lookup_tag_data).count() == len(tags)


@pytest.mark.django_db
class TestTagSerializer:
    def test_create_model(self, db):
        tag = TagFactory.build()
        serializer = TagSerializer(data=model_to_dict(tag))
        serializer.is_valid(raise_exception=True)
        model = serializer.save()
        assert Tag.objects.filter(slug=model.slug).exists()
