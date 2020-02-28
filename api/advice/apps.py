from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdviceConfig(AppConfig):
    name = "advice"
    verbose_name = _("advice")
