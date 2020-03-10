from factory import django as django_factory, faker, fuzzy, SubFactory
from api.users.tests import factories as user_factories
from api.advice.tests import factories as advice_factories

from ..models import Comment


class CommentFactory(django_factory.DjangoModelFactory):
    """
    Comment model factory
    """

    body = faker.Faker(
        "sentence", nb_words=6, variable_nb_words=True, ext_word_list=None
    )
    score = fuzzy.FuzzyDecimal(0, 10, 3)
    advice = SubFactory(advice_factories.AdviceFactory)
    author = SubFactory(user_factories.AccountFactory)

    class Meta:
        model = Comment
        django_get_or_create = ("body",)
