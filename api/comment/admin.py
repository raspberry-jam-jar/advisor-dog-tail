from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "advice", "created")
    search_fields = ("body", "author__email", "advice__title", "advice__slug")
