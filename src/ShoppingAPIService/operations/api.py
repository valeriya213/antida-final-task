from fastapi import FastAPI
from fastapi import APIRouter

router = APIRouter(prefix='/operations')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.post('')
def add_operation():
    pass


@router.get('')
def get_operations_for_period():
    pass


@router.get('/report')
def get_operations_report():
    pass
