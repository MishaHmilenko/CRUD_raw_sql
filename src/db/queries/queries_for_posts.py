from src.db.main import PgDataBase
from src.db.schemes.post import PostModel


def insert_into_post(post: PostModel, user_id: int):
    with PgDataBase() as db:
        db.cursor.execute("""
            INSERT INTO "post" (title, content, user_id, created_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP)
            RETURNING *
            """, (post.title, post.content, user_id))

        db.connection.commit()

        data = db.cursor.fetchone()

    return {
        'id': data[0],
        'title': data[1],
        'content': data[2],
        'created_at': data[3],
        'user_id': data[4]
    }


def select_post_by_id(post_id: int):
    with PgDataBase() as db:
        db.cursor.execute('SELECT * FROM "post" WHERE id = %s', (post_id,))

        data = db.cursor.fetchone()

        return {
            'id': data[0],
            'title': data[1],
            'content': data[2],
            'created_at': data[3],
            'user_id': data[4]
        }


def select_all_user_post_by_id(user_id: int):
    with PgDataBase() as db:
        db.cursor.execute('SELECT * FROM "post" WHERE user_id = %s', (user_id,))

        posts = db.cursor.fetchall()
        keys = ('id', 'title', 'content', 'created_at', 'user_id')

    return [zip(keys, post) for post in posts]


def update_post_by_id(post_id: int, post: PostModel):
    with PgDataBase() as db:
        db.cursor.execute('''
            UPDATE "post"
            SET title = %s, content = %s
            WHERE id = %s
            RETURNING id
            ''', (post.title, post.content, post_id))

        db.connection.commit()
        post_id = db.cursor.fetchone()[0]

        return select_post_by_id(post_id)
