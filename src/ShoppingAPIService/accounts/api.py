from fastapi import FastAPI
from fastapi import APIRouter

router = APIRouter(prefix='/singup')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.get('')
def authorization():
    pass
