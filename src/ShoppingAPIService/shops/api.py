from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from ..exseptions import EntityConflictError, EntiyDoesNotExistError
from ..accounts.schemas import Account
from ..accounts.auth import get_current_user
from .schemas import ShopName, Shop
from .service import ShopsServices


router = APIRouter(prefix='/shops')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.get('', response_model=List[Shop], tags=['Shops'])
def get_user_shops(
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    return shop_service.get_shops(current_account)


@router.post(
    '',
    response_model=Shop,
    status_code=status.HTTP_201_CREATED,
    tags=['Shops'],
)
def add_new_shop(
    new_shop: ShopName,
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    try:
        return shop_service.add_new_shop(new_shop, current_account)
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT)


@router.patch('/{shop_id}', response_model=Shop, tags=['Shops'])
def edit_shop(
    shop_id: int,
    shop: ShopName,
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    edit_shop = Shop(
        id=shop_id,
        name=shop.name,
    )
    try:
        return shop_service.edit_shop(edit_shop, current_account)
    except EntiyDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete(
    '/{shop_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Shops'],
)
def delete_shop(
    shop_id: int,
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    try:
        shop_service.delete_shop(shop_id, current_account)
        return Response()
    except EntiyDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
