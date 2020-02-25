from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as UserAdminBase
from django.utils.translation import gettext_lazy as _

from . import models


@admin.register(models.User)
class UserAdmin(UserAdminBase):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("email",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("username", "email", "is_bot", "is_staff")
    search_fields = ("username", "email")


@admin.register(models.Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("email", "created")
    search_fields = ("email",)
