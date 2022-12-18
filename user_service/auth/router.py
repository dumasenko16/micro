from datetime import timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from .jwt import create_access_token
from auth.schemas import User
from services import get_user_by_username


router = APIRouter(
    tags=['auth']
)


@router.post('/login')
async def login(
        request: OAuth2PasswordRequestForm = Depends(),
):
    user = await get_user_by_username(request.username)

    if user.password != request.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Password')

    access_token = create_access_token(data={"email": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
