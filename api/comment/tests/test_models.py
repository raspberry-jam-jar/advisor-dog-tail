import pytest

from .factories import CommentFactory


@pytest.mark.django_db
class TestCommentModel:
    def test_making_comment(self, db):
        comment = CommentFactory()
        assert CommentFactory._meta.model.objects.filter(
            advice=comment.advice, author=comment.author
        ).exists()
