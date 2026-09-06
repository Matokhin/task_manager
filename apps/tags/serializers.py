from rest_framework import serializers
from .models import Tag

class TagSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'title', 'created_by', 'created_at']
        read_only_fields = ['id', 'created_by', 'created_at']