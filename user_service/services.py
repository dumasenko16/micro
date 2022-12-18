import uuid
from models import User
import schemas
import utils


@utils.trace_it(tag='service', value='All users')
async def get_all_users() -> list[User]:
    return User.objects


@utils.trace_it(tag='service', value='Create user')
async def create_user(user: schemas.CreateUser) -> User:
    new_user = User(
        user_uuid=uuid.uuid4(),
        username=user.username,
        email=user.email,
        password=user.password,
    )
    new_user.save()
    return new_user


@utils.trace_it(tag='service', value='Get user by username')
async def get_user_by_username(input_email: str) -> User:
    return User.objects(email = input_email).first()
