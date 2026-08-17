from rest_framework import serializers
from .models import Task
from tags.models import Tag
from tags.serializers import TagSerializer
from comments.serializers import CommentSerializer


class TaskSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    assignee_username = serializers.CharField(source='assignee.username', read_only=True)

    status_display = serializers.CharField(source='get_status_display', read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)

    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        write_only=True,
        required=False,
        label="ID тегов"
    )

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'status_display',
            'priority',
            'priority_display',
            'project',
            'project_title',
            'assignee',
            'assignee_username',
            'created_at',
            'updated_at',
            'tags',
            'tag_ids',
            'comments',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']