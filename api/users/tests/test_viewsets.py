import pytest
import pytz

from datetime import timedelta, datetime
from http import HTTPStatus

from freezegun.api import FrozenDateTimeFactory
from django.contrib.auth import get_user_model

from rest_framework.test import APIRequestFactory, force_authenticate

from api.users.viewsets import AccountViewset
from api.users.models import Account

from .factories import AccountFactory


@pytest.mark.django_db
class TestAccountViewset:
    def test_add_account(
        self,
        db,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        account_vs: AccountViewset,
    ):
        account = AccountFactory.build()
        request = request_factory.post("/accounts/", {"email": account.email})
        force_authenticate(request, user=django_user)
        response = account_vs.as_view({"post": "create"})(request)
        assert response.status_code == HTTPStatus.CREATED
        assert Account.objects.filter(email=account.email).exists()

    def test_get_account_list(
        self,
        db,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        account_vs: AccountViewset,
    ):
        account = AccountFactory()
        request = request_factory.get("/accounts/")
        force_authenticate(request, user=django_user)
        response = account_vs.as_view({"get": "list"})(request)
        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["email"] == account.email

    def test_get_account(
        self,
        db,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        account_vs: AccountViewset,
    ):
        account = AccountFactory()
        request = request_factory.get(f"/accounts/{account.id}/")
        force_authenticate(request, user=django_user)
        response = account_vs.as_view({"get": "retrieve"})(request, pk=account.id)
        assert response.status_code == HTTPStatus.OK
        assert response.data["email"] == account.email

    def test_search_by_email(
        self,
        db,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        account_vs: AccountViewset,
    ):
        account = AccountFactory(email="admin@advdog.local")
        account_1 = AccountFactory(email="manager@advdog.local")  # noqa: F841

        request = request_factory.get(
            "/accounts/", {"search": account.email.split("@")[0].capitalize()}
        )
        force_authenticate(request, user=django_user)
        response = account_vs.as_view({"get": "list"})(request)

        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["email"] == account.email

    @pytest.mark.freeze_time(
        datetime(2020, 2, 25, 18, tzinfo=pytz.timezone("Europe/Moscow"))
    )
    def test_filter_by_created_from(
        self,
        db,
        freezer: FrozenDateTimeFactory,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        account_vs: AccountViewset,
    ):
        account = AccountFactory()
        freezer.move_to(account.created + timedelta(hours=2))
        account_2 = AccountFactory()  # noqa: F841

        created_from = account_2.created - timedelta(minutes=30)
        request = request_factory.get(
            "/accounts/",
            {"created_from": datetime.strftime(created_from, "%Y-%m-%d %H:%M:%S")},
        )
        force_authenticate(request, user=django_user)
        response = account_vs.as_view({"get": "list"})(request)
        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["email"] == account_2.email

    @pytest.mark.freeze_time(
        datetime(2020, 2, 25, 18, tzinfo=pytz.timezone("Europe/Moscow"))
    )
    def test_filter_by_created_to(
        self,
        db,
        freezer: FrozenDateTimeFactory,
        django_user: get_user_model(),
        request_factory: APIRequestFactory,
        account_vs: AccountViewset,
    ):
        account = AccountFactory()
        freezer.move_to(account.created + timedelta(hours=3))
        account_2 = AccountFactory()  # noqa: F841

        created_to = account.created + timedelta(hours=1)
        request = request_factory.get(
            "/accounts/",
            {"created_to": datetime.strftime(created_to, "%Y-%m-%d %H:%M:%S")},
        )
        force_authenticate(request, user=django_user)
        response = account_vs.as_view({"get": "list"})(request)
        assert response.status_code == HTTPStatus.OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["email"] == account.email
