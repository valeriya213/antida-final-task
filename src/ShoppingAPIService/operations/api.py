from datetime import date
from typing import List, Optional
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import Query
from fastapi import HTTPException
from fastapi import status

from ..accounts.schemas import Account
from ..accounts.auth import get_current_user
from ..exseptions import EntiyUnprocessableError
from .schemas import OperationRequest, Operation
from .service import OperationsServices

router = APIRouter(prefix='/operations')


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.post('', response_model=Operation)
def add_operation(
    new_operation: OperationRequest,
    current_account: Account = Depends(get_current_user),
    operation_services: OperationsServices = Depends(),
):
    try:
        operation = operation_services.add_operation(new_operation)
    except EntiyUnprocessableError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Operation(
        id=operation.id,
        type=operation.type,
        date=date.isoformat(operation.date),
        shop_id=operation.shop_id,
        category_id=operation.category_id,
        name=operation.name,
        price=operation.price,
        amount=operation.amount,
    )


@router.get('', response_model=List[Operation])
def get_operations_for_period(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    shops: Optional[List[int]] = Query(None),
    categories: Optional[List[int]] = Query(None),
    current_account: Account = Depends(get_current_user),
    operation_services: OperationsServices = Depends(),
):
    operations = operation_services.get_operations(
        current_account,
        date_from=date_from,
        date_to=date_to,
        shops=shops,
        categories=categories,
    )
    return [
        Operation(
            id=o.id,
            type=o.type,
            date=date.isoformat(o.date),
            shop_id=o.shop_id,
            category_id=o.category_id,
            name=o.name,
            price=o.price,
            amount=o.amount,
        )
        for o in operations
    ]


@router.get('/report')
def get_operations_report(
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    shops: Optional[List[int]] = Query(None),
    categories: Optional[List[int]] = Query(None),
    current_account: Account = Depends(get_current_user),
    operation_services: OperationsServices = Depends(),
):
    return operation_services.get_report(
        current_account,
        date_from=date_from,
        date_to=date_to,
        shops=shops,
        categories=categories,
    )
