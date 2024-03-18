from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.api.controllers.auth import utils

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/auth')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await utils.get_user_by_token(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    if not user['is_active']:
        raise HTTPException(
            status_code=400,
            detail='Inactive user'
        )
    return user
