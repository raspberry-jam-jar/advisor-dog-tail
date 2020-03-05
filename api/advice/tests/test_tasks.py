import pytest
import mock

from api.comment.tests import factories as comment_factories

from ..models.advice import Advice
from ..tasks import calculate_advice_mean_scores, calculate_advice_mean_score

from .factories import AdviceFactory


@pytest.mark.django_db
class TestAdviceTask:
    def _create_comment(self, **kwargs):
        return comment_factories.CommentFactory(**kwargs)

    def _create_10_comments_with_mean_around_6(self, advice):
        pairs = ((4, 9), (5, 10), (2, 7), (4, 9), (5, 8))
        comments = []
        for score_pair in pairs:
            for score in score_pair:
                comments.append(self._create_comment(advice=advice, score=score))
        return comments

    def _create_10_comments_with_mean_around_7(self, advice):
        pairs = ((6, 9), (5, 10), (5, 8), (7, 9), (5, 7))
        comments = []
        for score_pair in pairs:
            for score in score_pair:
                comments.append(self._create_comment(advice=advice, score=score))
        return comments

    def test_mean_score_calculating(self):
        advice = AdviceFactory()
        self._create_10_comments_with_mean_around_6(advice)

        task = calculate_advice_mean_score.apply(args=(advice.id,))
        assert task.status == "SUCCESS"

        advice = Advice.objects.filter(pk=advice.id).get()
        assert round(advice.score) == 6

    @mock.patch(
        "api.advice.tasks.calculate_advice_mean_score.delay",
        side_effect=lambda args: calculate_advice_mean_score(args[0]),
    )
    def test_batch_mean_score_calculating(self, subtests):

        advices = AdviceFactory.create_batch(4)

        mean_6_advices = advices[2:]
        for advice in mean_6_advices:
            self._create_10_comments_with_mean_around_6(advice)

        mean_7_advices = advices[:2]
        for advice in mean_7_advices:
            self._create_10_comments_with_mean_around_7(advice)

        task = calculate_advice_mean_scores.apply()
        assert task.status == "SUCCESS"

        with subtests.test(msg="test_advices_with_mean_6"):
            for advice in mean_6_advices:
                assert round(Advice.objects.filter(pk=advice.id).get().score) == 6

        with subtests.test(msg="test_advices_with_mean_7"):
            for advice in mean_7_advices:
                assert round(Advice.objects.filter(pk=advice.id).get().score) == 7
