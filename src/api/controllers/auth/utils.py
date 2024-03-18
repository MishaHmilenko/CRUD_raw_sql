import hashlib
import random
import string

from src.db.queries.queries_for_users import select_user_by_email, select_user_by_token, insert_into_user, insert_into_user_token
from src.db.schemes.auth import UserCreate


def get_random_string(length=12):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = get_random_string()
    enc = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split('$')
    return hash_password(password, salt) == hashed


def get_user_by_email(email: str):
    return select_user_by_email(email)


def get_user_by_token(token: str):
    return select_user_by_token(token)


def create_user_token(user_id):
    return insert_into_user_token(user_id)


def create_user(user: UserCreate):
    salt = get_random_string()
    hashed_password = hash_password(user.password, salt)
    return insert_into_user(user, f'{salt}${hashed_password}')
