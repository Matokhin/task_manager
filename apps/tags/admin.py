from django.contrib import admin
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_by', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)