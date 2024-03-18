from src.db.queries.queries_for_posts import insert_into_post, select_all_user_post_by_id, select_post_by_id, \
    update_post_by_id
from src.db.schemes.post import PostModel


def create_post(post: PostModel, user_id: int):
    return insert_into_post(post, user_id)


def get_user_post(post_id: int):
    return select_post_by_id(post_id)


def get_user_posts(user_id: int):
    return select_all_user_post_by_id(user_id)


def update_user_post(post_id: int, post_data: PostModel):
    return update_post_by_id(post_id, post_data)
