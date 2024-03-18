from fastapi import FastAPI

from .controllers.main import setup_controllers


def build_app():
    app = FastAPI(title='App')

    setup_controllers(app=app)

    return app
