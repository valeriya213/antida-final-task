from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Response
from fastapi import status

from ..accounts.schemas import Account
from ..accounts.auth import get_current_user
from ..exseptions import EntityConflictError, EntiyDoesNotExistError
from .schemas import Category, CategoryName
from .service import CategoryServices


router = APIRouter(prefix='/categories')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.get(
    '',
    response_model=List[Category],
    tags=['Categories'],
)
def get_user_categories(
    current_account: Account = Depends(get_current_user),
    category_service: CategoryServices = Depends(),
):
    return category_service.get_categories(current_account)


@router.post(
    '',
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
    tags=['Categories'],
)
def add_new_category(
    category_name: CategoryName,
    current_account: Account = Depends(get_current_user),
    category_service: CategoryServices = Depends(),
):
    try:
        return category_service.add_new_category(
            category_name,
            current_account,
        )
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT)


@router.patch('/{category_id}', response_model=Category, tags=['Categories'])
def edit_category(
    category_id: int,
    category_name: CategoryName,
    current_account: Account = Depends(get_current_user),
    category_service: CategoryServices = Depends(),
):
    edit_category = Category(
        id=category_id,
        name=category_name.name
    )
    try:
        return category_service.edit_category(edit_category, current_account)
    except EntiyDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)


@router.delete(
    '/{category_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['Categories'],
)
def delete_category(
    category_id: int,
    current_account: Account = Depends(get_current_user),
    category_service: CategoryServices = Depends(),
):
    try:
        category_service.delete_category(category_id, current_account)
        return Response()
    except EntiyDoesNotExistError:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
