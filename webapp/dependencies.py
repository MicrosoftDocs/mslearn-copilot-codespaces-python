from functools import lru_cache

from webapp.services.token_service import TokenService
from webapp.services.user_service import UserService


@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()


@lru_cache()
def get_user_service() -> UserService:
    return UserService()
