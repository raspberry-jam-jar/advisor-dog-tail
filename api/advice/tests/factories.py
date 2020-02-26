from factory import django as django_factory
from factory import faker

from ..models import Advice


class AdviceFactory(django_factory.DjangoModelFactory):
    """
    Advice model factory.
    """

    title = faker.Faker("name")
    link = faker.Faker("uri")

    class Meta:
        model = Advice
        django_get_or_create = ("title",)
