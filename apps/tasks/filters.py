from django_filters import rest_framework as filters
from .models import Task

class TaskFilter(filters.FilterSet):
    status = filters.CharFilter(field_name="status", lookup_expr="exact")
    priority = filters.CharFilter(field_name="priority", lookup_expr="exact")
    project = filters.NumberFilter(field_name="project_id", lookup_expr="exact")
    assignee = filters.NumberFilter(field_name="assignee_id", lookup_expr="exact")

    class Meta:
        model = Task
        fields = ['status', 'priority', 'project', 'assignee', 'tags']