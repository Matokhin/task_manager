import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProjects:

    def test_create_project_authenticated(self, auth_client):
        url = reverse('project-list')
        data = {"title": "New Awesome Project"}
        response = auth_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_project_list(self, auth_client, user, project_factory):
        project_factory.create_batch(2, owner=user)
        url = reverse('project-list')
        response = auth_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        if isinstance(response.data, dict) and 'results' in response.data:
            assert len(response.data['results']) == 2
        else:
            assert len(response.data) == 2

    def test_cannot_access_someone_elses_project(self, auth_client, project_factory):
        alien_project = project_factory()
        url = reverse('project-detail', kwargs={'pk': alien_project.pk})

        response = auth_client.get(url)
        assert response.status_code in [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND]