from fastapi import Depends

from ..config import Settings, get_settings
from ..database import Session, get_session
from .models import Shop


class ShopsServices():
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def add_new_shop(self, new_shop, current_user) -> Shop:
        shop = Shop(
            name=new_shop.name,
            account_id=current_user.id
        )
        self.session.add(shop)
        self.session.commit()
        return shop
