from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Task
from .serializers import TaskSerializer
from apps.comments.serializers import CommentSerializer
from .filters import TaskFilter

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