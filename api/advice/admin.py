from django.contrib import admin

from .models.advice import Advice
from .models.tag import Tag, TagType


# Register your models here.
@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "score",
        "created",
    )
    search_fields = ("title", "slug", "link")


@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    search_fields = ("title", "slug")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "created")
    search_fields = ("title",)
