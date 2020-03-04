from django.contrib import admin

from .models import Advice


# Register your models here.
@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "created",
    )
    search_fields = ("title", "slug", "link")
