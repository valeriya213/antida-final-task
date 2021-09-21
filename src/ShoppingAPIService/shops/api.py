from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI

from ..accounts.schemas import Account
from ..accounts.auth import get_current_user
from .schemas import Shop, ShopResponse
from .service import ShopsServices


router = APIRouter(prefix='/shops')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.get('', response_model=List[ShopResponse])
def get_user_shops(
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    pass


@router.post('', response_model=ShopResponse)
def add_new_shop(
    new_shop: Shop,
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    return shop_service.add_new_shop(new_shop, current_account)


@router.patch('/{shop_id}', response_model=ShopResponse)
def edit_shop(
    shop_id: int,
    shop: Shop,
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    pass


@router.delete('/{shop_id}')
def delete_shop(
    shop_id: int,
    shop: Shop,
    current_account: Account = Depends(get_current_user),
    shop_service: ShopsServices = Depends(),
):
    pass
