import pytest

from model_bakery import baker

from ..models import Advice
from ..serializers import AdviceSerializer, UpdateAdviceSerializer
from .factories import AdviceFactory


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
        for field in ("link", "slug", "author"):
            with subtests.test(msg=f"test_edit_{field}", i=field):
                advice = baker.make(Advice)
                field_data = {field: getattr(new_advice, field)}
                serializer = UpdateAdviceSerializer(
                    advice, data=field_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                assert not Advice.objects.filter(**field_data).exists()
