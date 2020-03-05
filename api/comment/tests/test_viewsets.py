import pytest

from http import HTTPStatus

from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate

from api.advice.models.advice import Advice
from api.users.models import Account

from ..viewsets import CommentViewSet
from ..models import Comment

from .factories import CommentFactory


# Create your tests here.
@pytest.mark.django_db
class TestCommentViewset:
    def test_create_comment(
        self,
        db,
        account: Account,
        advice: Advice,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        comment_vs: CommentViewSet,
    ):
        comment = CommentFactory.build(author=account, advice=advice)
        comment_data = {
            "body": comment.body,
            "advice": comment.advice.id,
            "author": comment.author.id,
        }
        request = request_factory.post("/comments/", comment_data, format="json")
        force_authenticate(request, user=django_user)
        response = comment_vs.as_view({"post": "create"})(request)
        assert response.status_code == HTTPStatus.CREATED
        assert Comment.objects.filter(
            author=comment.author, advice=comment.advice
        ).exists()

    def test_create_comment_with_score(
        self,
        db,
        account: Account,
        advice: Advice,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        comment_vs: CommentViewSet,
    ):
        comment = CommentFactory.build(author=account, advice=advice)
        comment_data = {
            "body": comment.body,
            "score": comment.score,
            "advice": comment.advice.id,
            "author": comment.author.id,
        }
        request = request_factory.post("/comments/", comment_data, format="json")
        force_authenticate(request, user=django_user)
        response = comment_vs.as_view({"post": "create"})(request)
        assert response.status_code == HTTPStatus.CREATED
        assert Comment.objects.filter(
            author=comment.author, advice=comment.advice
        ).exists()

    def test_update_comment(
        self,
        db,
        comment: Comment,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        comment_vs: CommentViewSet,
    ):
        new_comment = CommentFactory.build()
        comment_data = {"body": new_comment.body, "score": new_comment.score}
        request = request_factory.put(f"/comments/{comment.id}/", comment_data)
        force_authenticate(request, user=django_user)
        response = comment_vs.as_view({"put": "update"})(request, pk=comment.id)
        assert response.status_code == HTTPStatus.OK
        assert Comment.objects.filter(body=new_comment.body).exists()

    def test_partial_update_comment(
        self,
        db,
        subtests,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        comment_vs: CommentViewSet,
    ):
        new_comment = CommentFactory.build()
        for field in ("body", "score"):
            with subtests.test(msg=f"test_update_{field}", i=field):
                comment = CommentFactory()
                field_data = {field: getattr(new_comment, field)}
                request = request_factory.patch(f"/comments/{comment.pk}/", field_data)
                force_authenticate(request, user=django_user)
                response = comment_vs.as_view({"patch": "partial_update"})(
                    request, pk=comment.pk
                )
                assert response.status_code == HTTPStatus.OK
                assert Comment.objects.filter(**field_data).exists()

        # Forbid for updating
        for field in ("author", "advice"):
            with subtests.test(msg=f"test_update_{field}", i=field):
                comment = CommentFactory()
                field_data = {field: getattr(new_comment, field)}
                request = request_factory.patch(f"/comments/{comment.pk}/", field_data)
                force_authenticate(request, user=django_user)
                response = comment_vs.as_view({"patch": "partial_update"})(
                    request, pk=comment.pk
                )
                assert response.status_code == HTTPStatus.OK
                assert not Comment.objects.filter(**field_data).exists()

    def test_get_related_comments(
        self,
        db,
        advice: Advice,
        subtests,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        comment_vs: CommentViewSet,
    ):
        CommentFactory.create_batch(5, advice=advice)
        request = request_factory.get(f"/comments/advice/{advice.slug}/")
        force_authenticate(request, user=django_user)
        response = comment_vs.as_view({"get": "for_advice"})(
            request, advice_slug=advice.slug
        )
        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 5
        assert response.data["results"][0]["advice"] == advice.pk
