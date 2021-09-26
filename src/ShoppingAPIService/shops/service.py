from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..database import Session, get_session
from ..accounts.models import Account
from ..exseptions import EntityConflictError, EntiyDoesNotExistError
from .models import Shop
from .schemas import ShopName, Shop as ShopSchema


class ShopsServices():
    def __init__(
        self,
        session: Session = Depends(get_session),
    ):
        self.session = session

    def add_new_shop(self, new_shop: ShopName, current_user: Account) -> Shop:
        shop = Shop(
            name=new_shop.name,
            account_id=current_user.id,
        )
        self.session.add(shop)
        try:
            self.session.commit()
            return shop
        except IntegrityError:
            raise EntityConflictError

    def edit_shop(self, edit_shops: ShopSchema, current_user: Account) -> Shop:
        try:
            shop = self.session.execute(
                select(Shop)
                .where(Shop.id == edit_shops.id,
                       Shop.account_id == current_user.id)
            ).scalar_one()
        except NoResultFound:
            raise EntiyDoesNotExistError
        shop.name = edit_shops.name
        self.session.commit()
        return shop

    def get_shops(self, current_user: Account) -> List[Shop]:
        return self.session.execute(
            select(Shop)
            .where(Shop.account_id == current_user.id)
        ).scalars().all()

    def delete_shop(self, current_shop_id: int, current_user: Account):
        try:
            shop = self.session.execute(
                select(Shop)
                .where(Shop.id == current_shop_id,
                       Shop.account_id == current_user.id)
            ).scalar_one()
        except NoResultFound:
            raise EntiyDoesNotExistError
        self.session.delete(shop)
        self.session.commit()
