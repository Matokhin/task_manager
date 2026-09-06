import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserAndJWT:

    def test_successful_registration(self, api_client):
        url = reverse('auth_register')
        data = {
            "email": "example@example.com",
            "username": "newuser",
            "password": "StrongPassword123!"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(email=data["email"]).exists()

    def test_registration_with_existing_email(self, api_client, user):
        url = reverse('auth_register')
        data = {
            "email": user.email,
            "username": "distinct_username",
            "password": "StrongPassword123!"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_obtain_jwt_token_success(self, api_client, user):
        url = reverse('token_obtain_pair')
        data = {
            "email": user.email,
            "password": "password123"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_obtain_jwt_token_wrong_credentials(self, api_client, user):
        url = reverse('token_obtain_pair')
        data = {
            "email": user.email,
            "password": "wrong_password"
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED