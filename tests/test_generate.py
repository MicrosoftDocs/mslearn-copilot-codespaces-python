import pytest
from fastapi.testclient import TestClient

from webapp.main import app, get_token_service
from webapp.services.token_service import TokenService

client = TestClient(app)


def test_generate_default_length():
    response = client.post('/generate', json={})
    assert response.status_code == 200
    token = response.json()['token']
    assert isinstance(token, str)
    assert len(token) == 20


def test_generate_custom_length():
    response = client.post('/generate', json={'length': 10})
    assert response.status_code == 200
    assert len(response.json()['token']) == 10


def test_generate_length_one():
    response = client.post('/generate', json={'length': 1})
    assert response.status_code == 200
    assert len(response.json()['token']) == 1


def test_generate_large_length():
    response = client.post('/generate', json={'length': 64})
    assert response.status_code == 200
    assert len(response.json()['token']) == 64


def test_generate_zero_length():
    response = client.post('/generate', json={'length': 0})
    assert response.status_code == 200
    assert response.json()['token'] == ''


def test_generate_uses_injected_service():
    """Verify the endpoint uses the injected TokenService (override via DI)."""
    class FixedTokenService(TokenService):
        def generate(self, length: int = 20) -> str:
            return 'x' * length

    app.dependency_overrides[get_token_service] = lambda: FixedTokenService()
    try:
        response = client.post('/generate', json={'length': 5})
        assert response.json()['token'] == 'xxxxx'
    finally:
        app.dependency_overrides.clear()
