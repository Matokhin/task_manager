import hashlib
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.cache import cache
from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        query_params = urlencode(sorted(request.GET.items()))

        params_hash = hashlib.md5(query_params.encode()).hexdigest()

        cache_key = f"user_{request.user.id}_projects_list_{params_hash}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            response = Response(cached_data)
            response["X-Cache"] = "HIT"
            return response

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data_to_cache = self.get_paginated_response(serializer.data).data
            cache.set(cache_key, data_to_cache, timeout=600)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data_to_cache = serializer.data
        cache.set(cache_key, data_to_cache, timeout=600)

        response = Response(data_to_cache)
        response["X-Cache"] = "MISS"
        return response

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        self._clear_user_lists_cache()

    def perform_update(self, serializer):
        serializer.save()
        self._clear_user_lists_cache()
        cache.delete(f"project_detail_{serializer.instance.id}")

    def perform_destroy(self, instance):
        project_id = instance.id
        instance.delete()
        self._clear_user_lists_cache()
        cache.delete(f"project_detail_{project_id}")

    def _clear_user_lists_cache(self):
        self_user_id = self.request.user.id
        cache.delete_pattern(f"user_{self_user_id}_projects_list_*")