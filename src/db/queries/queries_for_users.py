from pydantic import EmailStr

from src.db.main import PgDataBase
from src.db.schemes.auth import UserCreate


def select_user_by_email(email: EmailStr):
    with PgDataBase() as db:
        db.cursor.execute('SELECT * FROM "user" WHERE email = %s', (email,))

        data = db.cursor.fetchone()

        if data is None:
            return None

    return {
        'id': data[0],
        'email': data[1],
        'username': data[2],
        'hashed_password': data[3]
    }


def select_user_by_token(token: str):
    with PgDataBase() as db:
        db.cursor.execute(f'''
        SELECT * FROM "user"
        JOIN "token" ON "user".id = "token".user_id
        WHERE "token".token = %s 
        AND "token".expires > NOW()
        ''', (token,))

        data = db.cursor.fetchone()
        print(data)

    return {
        'id': data[0],
        'username': data[1],
        'email': data[2],
        'is_active': data[4]
    }


def insert_into_user_token(user_id: int):
    with PgDataBase() as db:
        db.cursor.execute('''
        INSERT INTO "token" (expires, user_id)
        VALUES(NOW() +  INTERVAL '2 weeks', %s)
        ON CONFLICT (user_id)
        DO UPDATE SET token=gen_random_uuid(), expires=EXCLUDED.expires
        RETURNING token, expires;
        ''', (user_id,))
        db.connection.commit()

        data = db.cursor.fetchone()

    return {
        'token': data[0],
        'expires': data[1],
    }


def select_user_by_id(user_id):
    with PgDataBase() as db:
        db.cursor.execute('SELECT * FROM "user" WHERE id = %s', (user_id,))

        data = db.cursor.fetchone()

    return {
        'id': data[0],
        'email': data[1],
        'username': data[2],
    }


def insert_into_user(user: UserCreate, hashed_password):
    with PgDataBase() as db:
        db.cursor.execute('''
        INSERT INTO "user" (username, email, hashed_password)
        VALUES(%s, %s, %s)
        RETURNING id;
        ''', (user.username, user.email, hashed_password))

        db.connection.commit()

        user_id = db.cursor.fetchone()[0]
        data = select_user_by_id(user_id)

    return data


