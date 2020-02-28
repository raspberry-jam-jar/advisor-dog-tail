import pytest

from model_bakery import baker

from django.forms.models import model_to_dict

from ..serializers import (
    AdviceSerializer, UpdateAdviceSerializer, TagSerializer
)
from ..models.advice import Advice
from ..models.tag import Tag

from .factories import AdviceFactory, TagFactory


# Create your tests here.
@pytest.mark.django_db
class TestAdviceSerializer:
    def test_create_advice(self, db):
        advice = AdviceFactory.build()
        advice_data = {
            "title": advice.title,
            "link": advice.link,
            "author": {"email": advice.author.email},
        }
        serializer = AdviceSerializer(data=advice_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert Advice.objects.filter(title=advice.title).exists()

    def test_create_advice_with_new_tag(self, db):
        advice = AdviceFactory.build()
        tag = TagFactory.build()
        advice_data = model_to_dict(advice)
        advice_data["tags"] = [model_to_dict(tag)]
        serializer = AdviceSerializer(data=advice_data)
        serializer.is_valid(raise_exception=True)
        model = serializer.save()
        assert Advice.objects.filter(title=advice.title).exists()
        assert model.tags.count() == 1

    def test_update_advice(self, subtests, db):
        advice = AdviceFactory()
        new_advice = AdviceFactory.build()
        assert not Advice.objects.filter(title=new_advice.title).exists()
        serializer = UpdateAdviceSerializer(
            advice, data={"title": new_advice.title, "link": new_advice.link}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert not Advice.objects.filter(
            title=new_advice.title, link=new_advice.link
        ).exists()
        assert Advice.objects.filter(title=new_advice.title).exists()

    def test_partial_update_advice(self, subtests, db):
        new_advice = baker.prepare(Advice)
        for field in ("title",):
            with subtests.test(msg=f"test_edit_{field}", i=field):
                advice = baker.make(Advice)
                field_data = {field: getattr(new_advice, field)}
                serializer = UpdateAdviceSerializer(
                    advice, data=field_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                assert Advice.objects.filter(**field_data).exists()

        # Editing should be forbidden
        for field in ("link", "slug"):
            with subtests.test(msg=f"test_edit_{field}", i=field):
                advice = baker.make(Advice)
                field_data = {field: getattr(new_advice, field)}
                serializer = UpdateAdviceSerializer(
                    advice, data=field_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                assert not Advice.objects.filter(**field_data).exists()

        with subtests.test(msg="test_edit_author", i=new_advice.author.email):
            advice = baker.make(Advice)
            field_data = {"author": {"email": new_advice.author.email}}
            serializer = UpdateAdviceSerializer(advice, data=field_data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            assert not Advice.objects.filter(
                author__email=new_advice.author.email
            ).exists()

    def test_update_advice_tags_using_ru(self, db, user_tag):
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
    def test_create_tag(self, db):
        tag = TagFactory.build()
        serializer = TagSerializer(data=model_to_dict(tag))
        serializer.is_valid(raise_exception=True)
        model = serializer.save()
        assert Tag.objects.filter(slug=model.slug).exists()
