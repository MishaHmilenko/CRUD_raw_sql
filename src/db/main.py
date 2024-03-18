import psycopg

from abc import ABC, abstractmethod

from src.config import DB_HOST, DB_PORT, DB_NAME, DB_PASSWORD, DB_USER


class Database(ABC):

    def __init__(self, driver):
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()

    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.connection.close()


class PgDataBase(Database):

    def __init__(self):
        self.driver = psycopg
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )


def create_tables():
    with PgDataBase() as db:
        db.cursor.execute(f"""
        CREATE TABLE "user" (
            id SERIAL PRIMARY KEY,
            username VARCHAR(30),
            email VARCHAR(255) UNIQUE,
            hashed_password VARCHAR,
            is_active BOOLEAN NOT NULL DEFAULT TRUE 
        );
        """)

        db.cursor.execute(f"""
        CREATE TABLE "token" (
        id SERIAL PRIMARY KEY,
        token UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
        expires TIMESTAMP,
        user_id INTEGER UNIQUE REFERENCES "user"(id)
        );
        
        CREATE INDEX idx_tokens_user_id ON "token"(user_id);
        """)

        db.cursor.execute('''
        CREATE TABLE "post" (
        id SERIAL PRIMARY KEY,
        title VARCHAR,
        content TEXT,
        created_at TIMESTAMP,
        user_id INTEGER REFERENCES "user"(id)
        )
        ''')

        db.connection.commit()
        print('Tables are created successfully...')


def drop_tables():
    with PgDataBase() as db:
        db.cursor.execute('DROP TABLE IF EXISTS "user" CASCADE;')
        db.cursor.execute('DROP TABLE IF EXISTS "token" CASCADE;')

        db.connection.commit()
        print('Tables are dropped...')
