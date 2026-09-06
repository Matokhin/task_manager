import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from apps.projects.models import Project
from apps.tasks.models import Task

User = get_user_model()


@pytest.mark.django_db
class TestTaskCreation:

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(
            title="Test Project", owner=self.user
        )

        self.url = reverse("task-list")
        self.task1 = Task.objects.create(
            title="Fix bug in auth",
            description="Fix JWT token expiration issue",
            status="IN_PROGRESS",
            priority="HIGH",
            project=self.project,
            assignee=self.user,
        )
        self.task2 = Task.objects.create(
            title="Deploy application",
            description="Setup docker and deploy to production server",
            status="DONE",
            priority="HIGH",
            project=self.project,
            assignee=self.user,
        )
        self.task3 = Task.objects.create(
            title="Write documentation",
            description="Add README file for github repository",
            status="DONE",
            priority="LOW",
            project=self.project,
            assignee=self.user,
        )

    def test_filter_by_status(self, auth_client, user, project_factory, task_factory):
        """Тест фильтрации задач по статусу (?status=IN_PROGRESS)"""
        my_project = project_factory.create(owner=user)
        task_factory.create(project=my_project, status=Task.TaskStatus.DONE)
        task_factory.create(project=my_project, status=Task.TaskStatus.IN_PROGRESS)

        url = reverse('task-list')
        response = auth_client.get(url, {"status": Task.TaskStatus.DONE.value})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data.get('results', response.data)) == 1

    def test_filter_by_priority(self, auth_client, user, project_factory, task_factory):
        """Тест фильтрации задач по приоритету (?priority=HIGH)"""
        my_project = project_factory.create(owner=user)
        task_factory.create(project=my_project, priority=Task.TaskPriority.HIGH)

        url = reverse('task-list')
        response = auth_client.get(url, {"priority": Task.TaskPriority.HIGH.value})

        assert response.status_code == status.HTTP_200_OK

    def test_search_tasks(self, auth_client, user, project_factory, task_factory):
        """Тест текстового поиска по названию (?search=...)"""
        my_project = project_factory.create(owner=user)
        task_factory.create(project=my_project, title="Read documentation now")

        url = reverse('task-list')
        response = auth_client.get(url, {"search": "documentation"})

        assert response.status_code == status.HTTP_200_OK

    def test_order_tasks(self, auth_client, user, project_factory, task_factory):
        """Тест сортировки задач по названию (?ordering=title)"""
        my_project = project_factory.create(owner=user)
        task_factory.create(project=my_project, title="A_task")
        task_factory.create(project=my_project, title="B_task")

        url = reverse('task-list')
        response = auth_client.get(url, {"ordering": "title"})

        assert response.status_code == status.HTTP_200_OK

    def test_pagination(self, auth_client, user, project_factory, task_factory):
        """Тест работы кастомной пагинации"""
        my_project = project_factory.create(owner=user)

        task_factory.create_batch(20, project=my_project)

        url = reverse('task-list')
        response = auth_client.get(url, {"page": 1})

        assert response.status_code == status.HTTP_200_OK
        assert 'total_items' in response.data
        assert response.data['total_items'] == 20

    def test_combined_filters(self, auth_client, user, project_factory, task_factory):
        """Тест комбинирования нескольких фильтров одновременно"""
        my_project = project_factory.create(owner=user)
        task_factory.create(
            project=my_project,
            status=Task.TaskStatus.DONE,
            priority=Task.TaskPriority.HIGH
        )

        url = reverse('task-list')
        response = auth_client.get(
            url,
            {"status": Task.TaskStatus.DONE.value, "priority": Task.TaskPriority.HIGH.value}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_create_task_in_my_project(self, auth_client, user, project_factory):
        my_project = project_factory.create(owner=user)
        url = reverse('task-list')

        data = {
            "title": "Fix critical bug",
            "project": my_project.id,
            "status": "TODO",
            "priority": "HIGH"
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_cannot_create_task_in_alien_project(self, auth_client, project_factory):
        alien_project = project_factory.create()
        url = reverse('task-list')

        data = {
            "title": "Complete yesterday's task",
            "project": alien_project.id
        }
        response = auth_client.post(url, data, format='json')
        assert response.status_code in [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN]


@pytest.mark.django_db
class TestTaskFilteringAndPagination:

    def test_filter_tasks_by_status_and_priority(self, auth_client, user, project_factory, task_factory):
        """Проверка фильтрации задач по TextChoices значениям."""
        my_project = project_factory(owner=user)

        task_factory(project=my_project, status=Task.TaskStatus.IN_PROGRESS, priority=Task.TaskPriority.HIGH)
        task_factory(project=my_project, status=Task.TaskStatus.TODO, priority=Task.TaskPriority.LOW)
        task_factory(project=my_project, status=Task.TaskStatus.IN_PROGRESS, priority=Task.TaskPriority.LOW)

        url = reverse('task-list')

        query_params = {
            'status': Task.TaskStatus.IN_PROGRESS.value,
            'priority': Task.TaskPriority.LOW.value
        }
        response = auth_client.get(url, query_params)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['status'] == Task.TaskStatus.IN_PROGRESS.value

    def test_pagination_returns_correct_structure_and_limit(self, auth_client, user, project_factory, task_factory):
        """Проверка работы PageNumberPagination и структуры ответа."""
        my_project = project_factory(owner=user)
        task_factory.create_batch(15, project=my_project)

        url = reverse('task-list')
        response = auth_client.get(url, {'page': 1})

        assert response.status_code == status.HTTP_200_OK

        assert 'total_items' in response.data
        assert 'total_pages' in response.data
        assert 'current_page' in response.data
        assert 'page_size' in response.data
        assert 'links' in response.data
        assert 'results' in response.data

        assert 'next' in response.data['links']
        assert 'previous' in response.data['links']

        assert response.data['total_items'] == 15
        assert response.data['total_pages'] == 2
        assert response.data['current_page'] == 1
        assert response.data['page_size'] == 10
        assert len(response.data['results']) == 10

    def test_pagination_invalid_page_returns_404(self, auth_client, user, project_factory, task_factory):
        """Проверка поведения пагинации при передаче некорректной страницы."""
        my_project = project_factory(owner=user)
        task_factory.create_batch(5, project=my_project)

        url = reverse('task-list')
        response = auth_client.get(url, {'page': 9999})

        assert response.status_code == status.HTTP_404_NOT_FOUND