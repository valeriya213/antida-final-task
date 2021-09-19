from fastapi import FastAPI
from fastapi import APIRouter

router = APIRouter(prefix='/shops')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.get('')
def get_user_shops():
    pass


@router.post('')
def add_new_shop():
    pass


@router.patch('/{shop_id}')
def edit_shop(shop_id: int):
    pass


@router.delete('/{shop_id}')
def delete_shop(shop_id: int):
    pass
