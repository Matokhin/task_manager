import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestCommentsAndTags:

    def test_assign_multiple_tags_to_task(self, auth_client, user, project_factory, task_factory, tag_factory):
        my_project = project_factory(owner=user)
        my_task = task_factory(project=my_project)

        tag1 = tag_factory(title="backend")
        tag2 = tag_factory(title="django")

        url = reverse('task-detail', kwargs={'pk': my_task.pk})
        data = {
            "tag_ids": [tag1.id, tag2.id]
        }

        response = auth_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['tags']) == 2