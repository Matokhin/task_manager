import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCommentsAndTags:

    def test_create_comment(self, auth_client, user, project_factory, task_factory):
        my_project = project_factory.create(owner=user)
        my_task = task_factory.create(project=my_project)
        url = reverse('comment-list')

        data = {
            "text": "This is a test comment",
            "task": my_task.id
        }
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
