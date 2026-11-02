import re
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, field_validator

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def _check_email(value):
    if value is not None and not EMAIL_RE.match(value):
        raise ValueError('invalid email address')
    return value


class Body(BaseModel):
    length: Union[int, None] = 20


class UserCreate(BaseModel):
    name: str
    email: str

    _validate_email = field_validator('email')(_check_email)


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

    _validate_email = field_validator('email')(_check_email)


class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
