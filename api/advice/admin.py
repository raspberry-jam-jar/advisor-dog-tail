from django.contrib import admin

from .models import Advice, Tag


# Register your models here.
@admin.register(Advice)
class AdviceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "created",
    )
    search_fields = ("title", "slug", "link")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'created'
    )
    search_fields = ('title',)