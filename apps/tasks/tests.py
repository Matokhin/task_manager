from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.projects.models import Project
from .models import Task

User = get_user_model()


class TaskAPITestCase(APITestCase):

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

    def test_filter_by_status(self):
        """Тест фильтрации задач по статусу (?status=done)"""
        response = self.client.get(self.url, {"status": "DONE"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_items"], 2)
        for task in response.data["results"]:
            self.assertEqual(task["status"], "DONE")

    def test_filter_by_priority(self):
        """Тест фильтрации задач по приоритету (?priority=high)"""
        response = self.client.get(self.url, {"priority": "HIGH"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_items"], 2)
        for task in response.data["results"]:
            self.assertEqual(task["priority"], "HIGH")

    def test_search_tasks(self):
        """Тест текстового поиска по названию и описанию (?search=...)"""
        response = self.client.get(self.url, {"search": "documentation"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_items"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Write documentation")

        response_desc = self.client.get(self.url, {"search": "JWT"})
        self.assertEqual(response_desc.data["total_items"], 1)
        self.assertEqual(response_desc.data["results"][0]["title"], "Fix bug in auth")

    def test_order_tasks(self):
        """Тест сортировки задач по названию (?ordering=title)"""
        response = self.client.get(self.url, {"ordering": "title"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = response.data["results"]
        self.assertEqual(results[0]["title"], "Deploy application")
        self.assertEqual(results[1]["title"], "Fix bug in auth")
        self.assertEqual(results[2]["title"], "Write documentation")

    def test_pagination(self):
        """Тест работы кастомной пагинации"""
        for i in range(20):
            Task.objects.create(
                title=f"Extra Task {i}",
                status="IN_PROGRESS",
                priority="LOW",
                project=self.project,
                assignee=self.user,
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_items"], 23)
        self.assertEqual(response.data["total_pages"], 3)
        self.assertEqual(len(response.data["results"]), 10)

        response_page_2 = self.client.get(self.url, {"page": 2})
        self.assertEqual(len(response_page_2.data["results"]), 10)

    def test_combined_filters(self):
        """Тест комбинирования нескольких фильтров одновременно (?status=done&priority=high)"""
        response = self.client.get(
            self.url, {"status": "DONE", "priority": "HIGH"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_items"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Deploy application")