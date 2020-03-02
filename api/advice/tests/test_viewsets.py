import pytest
from http import HTTPStatus

from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate

from model_bakery import baker

from ..viewsets import AdviceViewSet
from ..models import Advice

from .factories import AdviceFactory


# Create your tests here.
@pytest.mark.django_db
class TestAdviceViewset:
    def test_create_advice(
        self,
        db,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        advice_vs: AdviceViewSet,
    ):
        advice = AdviceFactory.build()
        advice_data = {"title": advice.title, "link": advice.link}
        request = request_factory.post("/advices/", advice_data)
        force_authenticate(request, user=django_user)
        response = advice_vs.as_view({"post": "create"})(request)
        assert response.status_code == HTTPStatus.CREATED
        assert Advice.objects.filter(title=advice.title).exists()

    def test_update_advice(
        self,
        db,
        advice: Advice,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        advice_vs: AdviceViewSet,
    ):

        new_advice = AdviceFactory.build()
        advice_data = {"title": new_advice.title, "link": new_advice.link}
        request = request_factory.put(f"/advices/{advice.pk}/", advice_data)
        force_authenticate(request, user=django_user)
        response = advice_vs.as_view({"put": "update"})(request, pk=advice.pk)
        assert response.status_code == HTTPStatus.OK
        assert Advice.objects.filter(title=new_advice.title).exists()

    def test_partial_update_advice(
        self,
        db,
        subtests,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        advice_vs: AdviceViewSet,
    ):
        new_advice = baker.prepare(Advice)
        for field in ("title", "link"):
            with subtests.test(msg=f"test_update_{field}"):
                advice = baker.make(Advice)
                value = getattr(new_advice, field)
                request = request_factory.patch(
                    f"/advices/{advice.pk}/", {field: value}
                )
                force_authenticate(request, user=django_user)
                response = advice_vs.as_view({"patch": "partial_update"})(
                    request, pk=advice.pk
                )
                lookup_data = {field: value}
                assert response.status_code == HTTPStatus.OK
                assert Advice.objects.filter(**lookup_data).exists()

    def test_search_advice(
        self,
        db,
        subtests,
        advice: Advice,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        advice_vs: AdviceViewSet,
    ):
        usefull_advice = AdviceFactory(
            title="Полезная ссылка", link="https://www.google.com/"
        )
        usefull_advice.save()
        advice = AdviceFactory(title="Так себе", link="https://www.rambler.ru/")
        advice.save()

        request = request_factory.get("/advices/", {"search": "Полез"})
        force_authenticate(request, user=django_user)
        response = advice_vs.as_view({"get": "list"})(request)

        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["slug"] == usefull_advice.slug
