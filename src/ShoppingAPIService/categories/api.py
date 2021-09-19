from fastapi import FastAPI
from fastapi import APIRouter

router = APIRouter(prefix='/categories')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.get('')
def get_user_categories():
    pass


@router.post('')
def add_new_category():
    pass


@router.patch('/{category_id}')
def edit_category(category_id: int):
    pass


@router.delete('/{category_id}')
def delete_category(category_id: int):
    pass