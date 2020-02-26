import pytest

from django.forms.models import model_to_dict

from ..serializers import AdviceSerializer
from ..models import Advice

from .factories import AdviceFactory


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
