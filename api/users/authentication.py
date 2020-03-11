from django.conf import settings
from rest_framework import authentication

from .models import Account


class AccountAuthentication(authentication.BaseAuthentication):
    def get_account_header(self, headers: dict):
        return headers.get(settings.HTTP_ACCOUNT_HEADER, "")

    def authenticate(self, request):
        account = self.get_account_header(request.META).split()

        if len(account) == 0:
            return None

        try:
            email = account[1]
            instance = Account.objects.get(email=email)
            return (instance, email)
        except Account.DoesNotExist:
            return None
