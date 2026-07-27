from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "created_at", "updated_at")
    list_display_links = ("title",)
    search_fields = ("title", "description", "owner__username", "owner__email")
    list_filter = ("created_at", "owner")
    readonly_fields = ("created_at", "updated_at")
