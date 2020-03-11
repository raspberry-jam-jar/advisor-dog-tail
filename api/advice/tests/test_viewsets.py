import pytest

from http import HTTPStatus

from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate

from model_bakery import baker

from ..viewsets import AdviceViewSet
from ..models.advice import Advice
from ..models.tag import Tag

from .authentication import force_account
from .factories import AdviceFactory, TagFactory


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
        advice_data = {
            "title": advice.title,
            "link": advice.link,
            "author": {"email": advice.author.email},
        }
        request = request_factory.post("/advices/", advice_data, format="json")
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
        request = request_factory.put(f"/advices/{advice.slug}/", advice_data)
        force_authenticate(request, user=django_user)
        force_account(request, account=advice.author)
        response = advice_vs.as_view({"put": "update"})(request, slug=advice.slug)
        assert response.status_code == HTTPStatus.OK
        assert not Advice.objects.filter(slug=advice.slug).exists()
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
        for field in ("title",):
            with subtests.test(msg=f"test_update_{field}", i=field):
                advice = baker.make(Advice)
                field_data = {field: getattr(new_advice, field)}
                request = request_factory.patch(f"/advices/{advice.pk}/", field_data)
                force_authenticate(request, user=django_user)
                force_account(request, account=advice.author)
                response = advice_vs.as_view({"patch": "partial_update"})(
                    request, slug=advice.slug
                )
                assert response.status_code == HTTPStatus.OK
                assert Advice.objects.filter(**field_data).exists()

    def test_remove_advice_tag_by_slug(
        self,
        db,
        request_factory: APIRequestFactory,
        django_user: get_user_model(),
        advice: Advice,
        advice_vs: AdviceViewSet,
    ):
        video_tag = TagFactory(title="video")
        advice.tags.add(video_tag)
        request = request_factory.delete(
            f"/advices/{advice.slug}/tag/{video_tag.slug}/"
        )
        force_authenticate(request, user=django_user)
        force_account(request, account=advice.author)
        response = advice_vs.as_view({"delete": "tag"})(
            request, slug=advice.slug, tag_slug=video_tag.slug
        )

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert not advice.tags.filter(title=video_tag.title).exists()


@pytest.mark.django_db
class TestAdviceViewsetSearch:
    def test_search_using_ru(
        self,
        db,
        subtests,
        advice: Advice,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        advice_vs: AdviceViewSet,
    ):
        usefull_advice = baker.make(
            Advice, title="Полезная ссылка", link="https://www.google.com/"
        )
        advice = baker.make(  # noqa: F841
            Advice, title="Так себе", link="https://www.rambler.ru/"
        )

        request = request_factory.get("/advices/", {"search": "Полез"})
        force_authenticate(request, user=django_user)
        response = advice_vs.as_view({"get": "list"})(request)

        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["slug"] == usefull_advice.slug

    def test_search_by_tag_title(
        self,
        db,
        subtests,
        request_factory: APIRequestFactory,
        django_user: get_user_model(),
        user_tag: Tag,
        advice_vs: AdviceViewSet,
    ):
        cat_tag = TagFactory(title="cat")
        cat_advice = AdviceFactory(title="siam")
        cat_advice.tags.add(cat_tag)

        dog_tag = TagFactory(title="dog")
        dog_advice = AdviceFactory(title="corky")
        dog_advice.tags.add(dog_tag)

        with subtests.test(msg=f"test_search_advice_by_tag_slug", i=cat_tag.title):
            request = request_factory.get("/advices/", {"search": cat_tag.title})
            force_authenticate(request, user=django_user)
            response = advice_vs.as_view({"get": "list"})(request)

            assert response.status_code == HTTPStatus.OK
            assert response.data["count"] == 1
            assert response.data["results"][0]["slug"] == cat_advice.slug

        with subtests.test(msg=f"test_search_advice_by_tag_slug", i=dog_tag.title):
            request = request_factory.get("/advices/", {"search": dog_tag.title})
            force_authenticate(request, user=django_user)
            response = advice_vs.as_view({"get": "list"})(request)

            assert response.status_code == HTTPStatus.OK
            assert response.data["count"] == 1
            assert response.data["results"][0]["slug"] == dog_advice.slug

        with subtests.test(msg=f"test_search_advice_by_tag_slug", i=user_tag.title):
            request = request_factory.get("/advices/", {"search": user_tag.title})
            force_authenticate(request, user=django_user)
            response = advice_vs.as_view({"get": "list"})(request)

            assert response.status_code == HTTPStatus.OK
            assert response.data["count"] == 0

    def test_search_by_tag_entry(
        self,
        db,
        request_factory: APIRequestFactory,
        django_user: get_user_model(),
        advice: Advice,
        advice_vs: AdviceViewSet,
    ):
        desk_tag = TagFactory(title="desk")
        board_tag = TagFactory(title="board")
        party_tag = TagFactory(title="party")

        study_advice = AdviceFactory(title="Conspecting")

        for tag in (desk_tag, board_tag):
            study_advice.tags.add(tag)

        request = request_factory.get(
            "/advices/", {"search": f"{desk_tag.title} {party_tag.title}"}
        )
        force_authenticate(request, user=django_user)
        response = advice_vs.as_view({"get": "list"})(request)

        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["slug"] == study_advice.slug

    def test_search_order_by_multi_tags(
        self,
        db,
        request_factory: APIRequestFactory,
        django_user: get_user_model(),
        advice: Advice,
        advice_vs: AdviceViewSet,
    ):
        def get_pupel_tags(factory: TagFactory):
            return {
                title: factory(title=title)
                for title in ("teacher", "writing", "board", "conspecting", "party")
            }

        # Pupel tags
        tags = get_pupel_tags(TagFactory)

        conspecting_advice = AdviceFactory(title="Conspecting")

        for tag in ("teacher", "board", "writing", "conspecting"):
            conspecting_advice.tags.add(tags[tag])

        answering_advice = AdviceFactory(title="Public answer")

        for tag in ("teacher", "board"):
            answering_advice.tags.add(tags[tag])

        other_advice = AdviceFactory(title="Some stuff")
        other_advice.tags.add(tags["party"])

        search_string = " ".join(filter(lambda i: i != "writing", tags.keys()))
        request = request_factory.get("/advices/", {"search": search_string})
        force_authenticate(request, user=django_user)
        response = advice_vs.as_view({"get": "list"})(request)

        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 3
        # Advice must be ordered by tag amount which matched on the search request
        advices = enumerate((conspecting_advice, answering_advice, other_advice))
        for index, advice in advices:
            assert response.data["results"][index]["slug"] == advice.slug
