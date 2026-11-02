from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response

from webapp.dependencies import get_user_service
from webapp.models import User, UserCreate, UserUpdate
from webapp.services.user_service import UserService

router = APIRouter(prefix='/users', tags=['users'])


@router.post('', response_model=User, status_code=201)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create(data)


@router.get('', response_model=List[User])
def list_users(service: UserService = Depends(get_user_service)):
    return service.list()


@router.get('/{user_id}', response_model=User)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    user = service.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.put('/{user_id}', response_model=User)
def update_user(user_id: int, data: UserUpdate, service: UserService = Depends(get_user_service)):
    user = service.update(user_id, data)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.delete('/{user_id}', status_code=204)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    if not service.delete(user_id):
        raise HTTPException(status_code=404, detail='User not found')
    return Response(status_code=204)
