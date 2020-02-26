import pytz

from factory import django as django_factory
from factory import faker

from django.contrib.auth import get_user_model


class UserFactory(django_factory.DjangoModelFactory):
    """
    A user model factory
    """

    username = faker.Faker("user_name")
    email = faker.Faker("email")
    date_joined = faker.Faker("date_time", tzinfo=pytz.timezone("UTC"))
    is_staff = faker.Faker("random_element", elements=(0, 1))
    is_active = faker.Faker("random_element", elements=(0, 1))
    is_superuser = faker.Faker("random_element", elements=(0, 1))

    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)
