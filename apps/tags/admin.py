from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_by', 'created_at')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)