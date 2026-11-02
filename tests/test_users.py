import pytest

from webapp.models import UserCreate, UserUpdate


def test_service_crud(user_service):
    user = user_service.create(UserCreate(name='Ada', email='ada@example.com'))
    assert user.id == 1
    assert user_service.get(1) == user
    assert user_service.list() == [user]

    updated = user_service.update(1, UserUpdate(name='Ada L.'))
    assert updated.name == 'Ada L.'
    assert updated.email == 'ada@example.com'

    assert user_service.delete(1) is True
    assert user_service.delete(1) is False
    assert user_service.get(1) is None
    assert user_service.update(1, UserUpdate(name='x')) is None


def test_service_ids_increment(user_service):
    first = user_service.create(UserCreate(name='A', email='a@example.com'))
    second = user_service.create(UserCreate(name='B', email='b@example.com'))
    assert (first.id, second.id) == (1, 2)


def test_create_user(client):
    response = client.post('/users', json={'name': 'Ada', 'email': 'ada@example.com'})

    assert response.status_code == 201
    body = response.json()
    assert body['id'] == 1
    assert body['name'] == 'Ada'
    assert 'created_at' in body


def test_list_and_get_user(client):
    client.post('/users', json={'name': 'Ada', 'email': 'ada@example.com'})

    assert len(client.get('/users').json()) == 1
    assert client.get('/users/1').json()['email'] == 'ada@example.com'


def test_update_user_partial(client):
    client.post('/users', json={'name': 'Ada', 'email': 'ada@example.com'})

    response = client.put('/users/1', json={'name': 'Grace'})

    assert response.status_code == 200
    assert response.json()['name'] == 'Grace'
    assert response.json()['email'] == 'ada@example.com'


def test_delete_user(client):
    client.post('/users', json={'name': 'Ada', 'email': 'ada@example.com'})

    assert client.delete('/users/1').status_code == 204
    assert client.get('/users/1').status_code == 404


@pytest.mark.parametrize('method', ['get', 'delete'])
def test_missing_user_returns_404(client, method):
    assert getattr(client, method)('/users/99').status_code == 404


def test_update_missing_user_returns_404(client):
    assert client.put('/users/99', json={'name': 'x'}).status_code == 404


@pytest.mark.parametrize('payload', [
    {'name': 'Ada'},
    {'name': 'Ada', 'email': 'not-an-email'},
])
def test_create_invalid_payload_returns_422(client, payload):
    assert client.post('/users', json=payload).status_code == 422


def test_ping_still_works(client):
    assert client.get('/ping').json() == {'status': 'ok'}
