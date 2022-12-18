from fastapi import APIRouter, status, HTTPException, Depends

from schemas import User, CreateUser
import models
import utils
import services
import mapper

user_router = APIRouter(
    tags=['Users'],
    prefix='/users'
)


@user_router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[User],
)
@utils.trace_it(tag='', value='')
async def get_all_users() -> list[User]:
    users: list = await services.get_all_users()
    output = [
        mapper.mapping_model_schema(user)
        for user in users
    ]
    return output


@user_router.post(
    '/add',
    status_code=status.HTTP_201_CREATED,
    response_model=User
)
@utils.trace_it(tag='', value='')
async def create_user(user: CreateUser):
    u = await services.create_user(user)
    return mapper.mapping_model_schema(u)
