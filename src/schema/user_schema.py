from typing import List, Optional

from pydantic import BaseModel, EmailStr, SecretStr

from src.schema.base_schema import FindBase, ModelBaseInfo, SearchOptions
from src.util.schema import all_optional


class User(BaseModel):
    email: str
    user_token: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class BaseUser(BaseModel):
    email: str
    user_token: str
    name: str
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


class BaseUserWithPassword(BaseUser):
    password: str


@all_optional
class User(ModelBaseInfo, BaseUser):
    ...


@all_optional
class FindUser(FindBase, BaseUser):
    email__eq: str
    ...


@all_optional
class UpsertUser(BaseUser):
    ...


class FindUserResult(BaseModel):
    founds: Optional[List[User]]
    search_options: Optional[SearchOptions]
