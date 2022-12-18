from pydantic import BaseModel
from uuid import UUID


class BaseUser(BaseModel):
    username: str
    email: str
    password: str


class CreateUser(BaseUser):
    pass


class User(BaseUser):
    user_uuid: UUID
