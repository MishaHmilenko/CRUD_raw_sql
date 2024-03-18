from fastapi import APIRouter, HTTPException, Depends

from src.api.dependencies.auth import get_current_user
from src.db.schemes.auth import User
from src.db.schemes.post import PostModel
from src.api.controllers.posts import utils

router = APIRouter(prefix='/posts', tags=['post'])


@router.post('/create-post')
def create_post(post: PostModel, current_user: User = Depends(get_current_user)):
    post = utils.create_post(post, current_user['id'])
    return post


@router.get('/{user_id}')
def get_user_post(user_id: int):
    posts = utils.get_user_posts(user_id)
    return posts


@router.put('/{post_id}')
def update_post(
        post_id: int, post_data: PostModel, current_user=Depends(get_current_user)
):
    post = utils.get_user_post(post_id)

    if post['user_id'] != current_user['id']:
        raise HTTPException(
            status_code=403,
            detail='You don\'t have access to modify this post'
        )

    return utils.update_user_post(post_id, post_data)
