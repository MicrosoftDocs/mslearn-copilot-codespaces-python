import uuid
from typing import Optional

from webapp.models.user import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self) -> None:
        self._store: dict[str, UserResponse] = {}

    def create(self, data: UserCreate) -> UserResponse:
        user = UserResponse(id=str(uuid.uuid4()), username=data.username, email=data.email)
        self._store[user.id] = user
        return user

    def get_all(self) -> list[UserResponse]:
        return list(self._store.values())

    def get_by_id(self, user_id: str) -> Optional[UserResponse]:
        return self._store.get(user_id)

    def update(self, user_id: str, data: UserUpdate) -> Optional[UserResponse]:
        user = self._store.get(user_id)
        if user is None:
            return None
        updated = user.model_copy(update={k: v for k, v in data.model_dump().items() if v is not None})
        self._store[user_id] = updated
        return updated

    def delete(self, user_id: str) -> bool:
        if user_id not in self._store:
            return False
        del self._store[user_id]
        return True
