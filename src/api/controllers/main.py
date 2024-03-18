from fastapi import FastAPI
from .task import router as task_router
from .auth.users import router as users_router
from .posts.posts import router as post_router


def setup_controllers(app: FastAPI):
    app.include_router(router=task_router)
    app.include_router(router=users_router)
    app.include_router(router=post_router)
