from factory import django as django_factory, faker, SubFactory, fuzzy
from api.users.tests import factories

from ..models.advice import Advice
from ..models.tag import TagType, Tag


class TagTypeFactory(django_factory.DjangoModelFactory):
    """
    Tag type model factory.
    """

    title = faker.Faker("slug")

    class Meta:
        model = TagType
        django_get_or_create = ("title",)


class TagFactory(django_factory.DjangoModelFactory):
    """
    Tag model factory
    """

    title = faker.Faker("slug")

    class Meta:
        model = Tag
        django_get_or_create = ("title",)


class AdviceFactory(django_factory.DjangoModelFactory):
    """
    Advice model factory.
    """

    title = faker.Faker("slug")
    link = faker.Faker("uri")
    score = fuzzy.FuzzyDecimal(0, 10, 3)
    author = SubFactory(factories.AccountFactory)

    class Meta:
        model = Advice
        django_get_or_create = ("title",)
