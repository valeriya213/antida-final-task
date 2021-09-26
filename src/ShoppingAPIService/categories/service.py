from typing import List
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from ..database import Session, get_session
from ..accounts.models import Account
from ..exseptions import EntityConflictError, EntiyDoesNotExistError
from .models import Category
from .schemas import CategoryName, Category as CategorySchemas


class CategoryServices():
    def __init__(
        self,
        session: Session = Depends(get_session),
    ):
        self.session = session

    def add_new_category(
        self,
        new_category: CategoryName,
        current_user: Account,
    ) -> Category:
        category = Category(
            name=new_category.name,
            account_id=current_user.id,
        )
        self.session.add(category)
        try:
            self.session.commit()
            return category
        except IntegrityError:
            raise EntityConflictError

    def edit_category(
        self,
        edit_category: CategorySchemas,
        current_user: Account,
    ) -> Category:
        try:
            category = self.session.execute(
                select(Category)
                .where(Category.id == edit_category.id,
                       Category.account_id == current_user.id)
            ).scalar_one()
        except NoResultFound:
            raise EntiyDoesNotExistError
        category.name = edit_category.name
        self.session.commit()
        return category

    def get_categories(self, current_user: Account) -> List[Category]:
        return self.session.execute(
            select(Category)
            .where(Category.account_id == current_user.id)
        ).scalars().all()

    def delete_category(self, current_category_id: int, current_user: Account):
        try:
            category = self.session.execute(
                select(Category)
                .where(Category.id == current_category_id,
                       Category.account_id == current_user.id)
            ).scalar_one()
        except NoResultFound:
            raise EntiyDoesNotExistError
        self.session.delete(category)
        self.session.commit()
