import pytest
from fastapi.testclient import TestClient

from webapp.dependencies import get_token_service, get_user_service
from webapp.main import app
from webapp.services.token_service import TokenService
from webapp.services.user_service import UserService


@pytest.fixture
def user_service():
    return UserService()


@pytest.fixture
def client(user_service):
    app.dependency_overrides[get_user_service] = lambda: user_service
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def mock_token_service(mocker):
    mock = mocker.Mock(spec=TokenService)
    app.dependency_overrides[get_token_service] = lambda: mock
    return mock
