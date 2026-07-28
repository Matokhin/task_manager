from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'task', 'created_at')
    list_display_links = ('id',)
    search_fields = ('text', 'author__username', 'task__title')
    list_filter = ('created_at', 'author')
    readonly_fields = ('created_at',)