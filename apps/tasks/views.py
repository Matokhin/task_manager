from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from apps.projects.models import Project
from .models import Task
from .serializers import TaskSerializer
from apps.comments.serializers import CommentSerializer
from .filters import TaskFilter
from .pagination import TaskPagination
from .tasks import task_creation_log


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    @action(
        detail=True,
        methods=['get', 'post'],
        permission_classes=[permissions.IsAuthenticatedOrReadOnly],
        url_path='comments'
    )
    def comments(self, request, pk=None):

        task = self.get_object()

        # --- ОБРАБОТКА GET-ЗАПРОСА ---
        if request.method == 'GET':
            comments = task.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # --- ОБРАБОТКА POST-ЗАПРОСА ---
        if request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, task=task)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    pagination_class = TaskPagination

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')

        if not project_id:
            raise ValidationError({"project": "Это поле обязательно."})
        try:
            project = Project.objects.get(id=project_id, owner=self.request.user)
        except Project.DoesNotExist:
            raise ValidationError({"project": "Проект не найден или у вас нет к нему доступа."})

        task = serializer.save(assignee=self.request.user, project=project)

        task_creation_log.delay(
            task_id=task.id,
            title=task.title,
            assignee=self.request.user.username
        )