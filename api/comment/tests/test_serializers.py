import pytest

from ..serializers import CommentSerializer, UpdateCommentSerializer
from ..models import Comment

from .factories import CommentFactory


@pytest.mark.django_db
class TestCommentSerializer:
    def test_create_comment(self, db):
        comment = CommentFactory.build()
        comment.author.save()
        comment.advice.author = comment.author
        comment.advice.save()
        advice_data = {
            "body": comment.body,
            "author": comment.author.id,
            "advice": comment.advice.id,
        }
        serializer = CommentSerializer(data=advice_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert Comment.objects.filter(
            advice=comment.advice, author=comment.author
        ).exists()

    def test_update_comment(self, db):
        comment = CommentFactory()
        new_comment = CommentFactory.build()
        comment_data = {
            "body": new_comment.body,
            "score": new_comment.score,
            "advice": new_comment.advice.id,
            "author": new_comment.author.id,
        }
        serializer = UpdateCommentSerializer(comment, data=comment_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        assert not Comment.objects.filter(
            advice=new_comment.advice, author=new_comment.author
        ).exists()
        assert Comment.objects.filter(body=new_comment.body).exists()

    def test_partial_update_advice(self, subtests, db):
        new_comment = CommentFactory.build()
        for field in ("score", "body"):
            with subtests.test(msg=f"test_edit_{field}", i=field):
                comment = CommentFactory()
                field_data = {field: getattr(new_comment, field)}
                serializer = UpdateCommentSerializer(
                    comment, data=field_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                assert Comment.objects.filter(**field_data).exists()

        # Editing should be forbidden
        for field in ("author", "advice"):
            with subtests.test(msg=f"test_edit_{field}", i=field):
                comment = CommentFactory()
                field_data = {field: getattr(new_comment, field)}
                serializer = UpdateCommentSerializer(
                    comment, data=field_data, partial=True
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                assert not Comment.objects.filter(**field_data).exists()
