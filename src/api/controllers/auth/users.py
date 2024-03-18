from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.api.controllers.auth import utils
from src.api.dependencies.auth import get_current_user
from src.db.schemes.auth import User, UserCreate

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/sign-up')
def create_user(user: UserCreate):
    db_user = utils.get_user_by_email(email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    return utils.create_user(user=user)


@router.post('/auth')
def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = utils.get_user_by_email(email=form_data.username)  # В поле формы userame вписывается почта

    if not user:
        raise HTTPException(status_code=404, detail='Incorrect email or password')

    if not utils.validate_password(
            password=form_data.password, hashed_password=user['hashed_password']
    ):
        raise HTTPException(status_code=404, detail='Incorrect email or password')

    return utils.create_user_token(user_id=user['id'])


@router.get('/me')
def get_users_me(current_user: User = Depends(get_current_user)):
    return current_user
