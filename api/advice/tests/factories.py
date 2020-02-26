from factory import (
    django as django_factory,
    faker,
    SubFactory
)

from api.users.tests import factories

from ..models import Advice


class AdviceFactory(django_factory.DjangoModelFactory):
    """
    Advice model factory.
    """

    title = faker.Faker("name")
    link = faker.Faker("uri")
    author = SubFactory(factories.AccountFactory)

    class Meta:
        model = Advice
        django_get_or_create = ("title",)
