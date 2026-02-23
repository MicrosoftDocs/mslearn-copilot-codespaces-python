import pytest
from fastapi.testclient import TestClient

from webapp.main import app, get_user_service
from webapp.services.user_service import UserService

# Each test gets a fresh UserService to avoid state leakage
@pytest.fixture(autouse=True)
def fresh_user_service():
    service = UserService()
    app.dependency_overrides[get_user_service] = lambda: service
    yield service
    app.dependency_overrides.clear()


client = TestClient(app)


# --- Create ---

def test_create_user():
    response = client.post('/users', json={'username': 'alice', 'email': 'alice@example.com'})
    assert response.status_code == 201
    data = response.json()
    assert data['username'] == 'alice'
    assert data['email'] == 'alice@example.com'
    assert 'id' in data


# --- List ---

def test_list_users_empty():
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json() == []


def test_list_users_returns_created():
    client.post('/users', json={'username': 'alice', 'email': 'alice@example.com'})
    client.post('/users', json={'username': 'bob', 'email': 'bob@example.com'})
    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json()) == 2


# --- Get by ID ---

def test_get_user_by_id():
    created = client.post('/users', json={'username': 'alice', 'email': 'alice@example.com'}).json()
    response = client.get(f"/users/{created['id']}")
    assert response.status_code == 200
    assert response.json()['id'] == created['id']


def test_get_user_not_found():
    response = client.get('/users/nonexistent-id')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


# --- Update ---

def test_update_user():
    created = client.post('/users', json={'username': 'alice', 'email': 'alice@example.com'}).json()
    response = client.put(f"/users/{created['id']}", json={'username': 'alice2'})
    assert response.status_code == 200
    data = response.json()
    assert data['username'] == 'alice2'
    assert data['email'] == 'alice@example.com'  # unchanged


def test_update_user_not_found():
    response = client.put('/users/nonexistent-id', json={'username': 'ghost'})
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'


# --- Delete ---

def test_delete_user():
    created = client.post('/users', json={'username': 'alice', 'email': 'alice@example.com'}).json()
    response = client.delete(f"/users/{created['id']}")
    assert response.status_code == 204
    # Confirm it's gone
    assert client.get(f"/users/{created['id']}").status_code == 404


def test_delete_user_not_found():
    response = client.delete('/users/nonexistent-id')
    assert response.status_code == 404
    assert response.json()['detail'] == 'User not found'
