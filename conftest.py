import pytest
import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

pytest_plugins = ["pytest_django"]

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    username = factory.Sequence(lambda n: f"user_{n}")
    password = factory.PostGenerationMethodCall("set_password", "password123")


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = "projects.Project"

    title = factory.Sequence(lambda n: f"Project {n}")
    owner = factory.SubFactory(UserFactory)


class TagFactory(DjangoModelFactory):
    class Meta:
        model = "tags.Tag"

    title = factory.Sequence(lambda n: f"tag_{n}")


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = "tasks.Task"

    title = factory.Sequence(lambda n: f"Task {n}")
    project = factory.SubFactory(ProjectFactory)
    status = "TODO"
    priority = "MEDIUM"


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = "comments.Comment"

    text = factory.Sequence(lambda n: f"Comment content {n}")
    task = factory.SubFactory(TaskFactory)
    author = factory.SubFactory(UserFactory)


@pytest.fixture
def user_factory(db):
    return UserFactory


@pytest.fixture
def project_factory(db):
    return ProjectFactory


@pytest.fixture
def task_factory(db):
    return TaskFactory


@pytest.fixture
def tag_factory(db):
    return TagFactory


@pytest.fixture
def comment_factory(db):
    return CommentFactory


# --- Клиенты ---

@pytest.fixture
def api_client(db):
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory.create()


@pytest.fixture
def auth_client(db, user):
    from rest_framework.test import APIClient
    from rest_framework_simplejwt.tokens import RefreshToken

    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client