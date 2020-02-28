from factory import django as django_factory
from factory import faker

from ..models.advice import Advice
from ..models.tag import Tag


class TagTypeFactory(django_factory.DjangoModelFactory):
    """
    Tag type model factory.
    """

    title = faker.Faker("slug")

    class Meta:
        model = Tag
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

    class Meta:
        model = Advice
        django_get_or_create = ("title",)
