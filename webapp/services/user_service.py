from datetime import datetime, timezone
from typing import Dict, List, Optional

from webapp.models import User, UserCreate, UserUpdate


class UserService:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._next_id = 1

    def create(self, data: UserCreate) -> User:
        user = User(
            id=self._next_id,
            name=data.name,
            email=data.email,
            created_at=datetime.now(timezone.utc),
        )
        self._users[user.id] = user
        self._next_id += 1
        return user

    def get(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def list(self) -> List[User]:
        return [*self._users.values()]

    def update(self, user_id: int, data: UserUpdate) -> Optional[User]:
        user = self._users.get(user_id)
        if user is None:
            return None
        changes = data.model_dump(exclude_unset=True, exclude_none=True)
        updated = user.model_copy(update=changes)
        self._users[user_id] = updated
        return updated

    def delete(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None
