from typing import Annotated, Union
from math import ceil
from os.path import dirname, abspath, join
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from webapp.models.token import PaginatedResponse
from webapp.models.user import UserCreate, UserUpdate, UserResponse
from webapp.services.token_service import TokenService
from webapp.services.user_service import UserService

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")

MAX_TOKENS = 1000

# Singleton service instances shared across requests
_token_service = TokenService()
_user_service = UserService()


def get_token_service() -> TokenService:
    return _token_service


def get_user_service() -> UserService:
    return _user_service


class Body(BaseModel):
    length: Union[int, None] = 20


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.post('/generate')
def generate(body: Body, service: TokenService = Depends(get_token_service)):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    return {'token': service.generate(body.length)}


@app.post('/generate/paginated', response_model=PaginatedResponse)
def generate_paginated(
    body: Body,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    service: TokenService = Depends(get_token_service),
):
    """
    Generate a paginated list of pseudo-random token IDs.

    - **page**: page number (1-indexed)
    - **page_size**: number of tokens per page (1–100)
    - **total**: server-side cap of 1000 tokens
    """
    total = MAX_TOKENS
    total_pages = ceil(total / page_size)
    offset = (page - 1) * page_size
    items_count = max(0, min(page_size, total - offset))
    items = [service.generate(body.length) for _ in range(items_count)]
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )


@app.get('/ping')
def ping():
    return {'status': 'ok'}


@app.get('/health')
def health():
    return {'status': 'healthy'}


# --- User CRUD ---

@app.post('/users', response_model=UserResponse, status_code=201)
def create_user(body: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create(body)


@app.get('/users', response_model=list[UserResponse])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all()


@app.get('/users/{user_id}', response_model=UserResponse)
def get_user(user_id: str, service: UserService = Depends(get_user_service)):
    user = service.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.put('/users/{user_id}', response_model=UserResponse)
def update_user(user_id: str, body: UserUpdate, service: UserService = Depends(get_user_service)):
    user = service.update(user_id, body)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.delete('/users/{user_id}', status_code=204)
def delete_user(user_id: str, service: UserService = Depends(get_user_service)):
    if not service.delete(user_id):
        raise HTTPException(status_code=404, detail="User not found")