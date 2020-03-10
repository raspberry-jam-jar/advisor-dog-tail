from celery import task
from celery.utils.log import get_task_logger

from django.db import transaction

from api.comment.models import Comment

from .models.advice import Advice

logger = get_task_logger(__name__)


@task(bind=True)
def calculate_advice_mean_score(self, advice: str):
    """
    Calculate a mean score for the current advice.
    :param advice: advice uuid
    """
    logger.info(f"Start calculating the mean score for the {advice} advice.")
    score = 0
    with transaction.atomic():
        score = Comment.objects.select_for_update().advice_mean_score(advice)
    with transaction.atomic():
        (Advice.objects.select_for_update().filter(pk=advice).update(score=score))
    logger.info(f"The current mean score for" " advice {advice_id} is {score}.")


@task(bind=True)
def calculate_advice_mean_scores(self):
    logger.info(f"Start calculating the mean score for each advice.")
    for row in Advice.objects.values("id").all():
        calculate_advice_mean_score.delay(args=(row["id"],))
    logger.info(f"Mean scores have been made for each advice.")
