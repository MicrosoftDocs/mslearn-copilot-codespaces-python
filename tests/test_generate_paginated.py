import pytest
from math import ceil
from fastapi.testclient import TestClient

from webapp.main import app, get_token_service, MAX_TOKENS
from webapp.services.token_service import TokenService

client = TestClient(app)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def post_paginated(page=None, page_size=None, body=None):
    params = {}
    if page is not None:
        params['page'] = page
    if page_size is not None:
        params['page_size'] = page_size
    return client.post('/generate/paginated', json=body or {}, params=params)


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------

def test_paginated_default_params():
    response = post_paginated()
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 10
    assert data['page'] == 1
    assert data['page_size'] == 10
    assert data['total'] == MAX_TOKENS
    assert data['total_pages'] == ceil(MAX_TOKENS / 10)


def test_paginated_custom_page_size():
    response = post_paginated(page_size=5)
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == 5
    assert data['page_size'] == 5


def test_paginated_custom_page():
    response = post_paginated(page=3, page_size=10)
    assert response.status_code == 200
    data = response.json()
    assert data['page'] == 3
    assert len(data['items']) == 10


def test_paginated_custom_token_length():
    response = post_paginated(page_size=4, body={'length': 8})
    assert response.status_code == 200
    for token in response.json()['items']:
        assert len(token) == 8


def test_paginated_last_page():
    # MAX_TOKENS=1000, page_size=7 → total_pages=ceil(1000/7)=143, last page has 1000 - 142*7 = 6 items
    page_size = 7
    total_pages = ceil(MAX_TOKENS / page_size)
    expected_last = MAX_TOKENS - (total_pages - 1) * page_size
    response = post_paginated(page=total_pages, page_size=page_size)
    assert response.status_code == 200
    data = response.json()
    assert len(data['items']) == expected_last
    assert data['total_pages'] == total_pages


def test_paginated_beyond_last_page():
    total_pages = ceil(MAX_TOKENS / 10)
    response = post_paginated(page=total_pages + 1, page_size=10)
    assert response.status_code == 200
    data = response.json()
    assert data['items'] == []


def test_paginated_total_pages_math():
    for page_size in [1, 7, 10, 33, 100]:
        response = post_paginated(page_size=page_size)
        assert response.json()['total_pages'] == ceil(MAX_TOKENS / page_size)


# ---------------------------------------------------------------------------
# Validation (422)
# ---------------------------------------------------------------------------

def test_paginated_page_zero_returns_422():
    response = post_paginated(page=0)
    assert response.status_code == 422


def test_paginated_page_size_zero_returns_422():
    response = post_paginated(page_size=0)
    assert response.status_code == 422


def test_paginated_page_size_over_max_returns_422():
    response = post_paginated(page_size=101)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# DI override
# ---------------------------------------------------------------------------

def test_paginated_uses_injected_service():
    """Verify the paginated endpoint honours the injected TokenService."""
    class FixedTokenService(TokenService):
        def generate(self, length: int = 20) -> str:
            return 'x' * length

    app.dependency_overrides[get_token_service] = lambda: FixedTokenService()
    try:
        response = post_paginated(page_size=3, body={'length': 4})
        assert response.status_code == 200
        assert response.json()['items'] == ['xxxx', 'xxxx', 'xxxx']
    finally:
        app.dependency_overrides.clear()
