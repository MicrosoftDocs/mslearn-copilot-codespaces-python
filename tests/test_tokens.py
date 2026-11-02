from webapp.services.token_service import TokenService


def test_default_length():
    assert len(TokenService().generate()) == 20


def test_custom_length():
    assert len(TokenService().generate(8)) == 8


def test_tokens_differ():
    service = TokenService()
    assert service.generate() != service.generate()


def test_generate_endpoint_uses_injected_service(client, mock_token_service):
    mock_token_service.generate.return_value = 'abc'

    response = client.post('/generate', json={'length': 3})

    assert response.status_code == 200
    assert response.json() == {'token': 'abc'}
    mock_token_service.generate.assert_called_once_with(3)


def test_generate_endpoint_default_length(client):
    response = client.post('/generate', json={})

    assert response.status_code == 200
    assert len(response.json()['token']) == 20
