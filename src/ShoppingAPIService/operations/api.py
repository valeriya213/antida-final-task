from typing import List
from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status

from ..accounts.schemas import Account
from ..accounts.auth import get_current_user
from ..exseptions import EntiyUnprocessableError
from .schemas import OperationRequest, Operation
from .service import OperationsServices
from .queryparams import QueryParams, get_query_params

router = APIRouter(prefix='/operations')


def initialize_app(app: FastAPI):
    app.include_router(router)


description = """To filter, specify the parameters in format
(all parameters are optional):
?date_from=2020-01-01&date_to=2021-01-01&shops=1,2,3&categories=1,2,3
"""

@router.post(
    '',
    response_model=Operation,
    status_code=status.HTTP_201_CREATED,
    tags=['Operations'])
def add_operation(
    new_operation: OperationRequest,
    current_account: Account = Depends(get_current_user),
    operation_services: OperationsServices = Depends(),
):
    try:
        return operation_services.add_operation(
            new_operation,
            current_account,
        )
    except EntiyUnprocessableError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)


@router.get(
    '',
    response_model=List[Operation],
    description=description,
    tags=['Operations'],
)
def get_operations_for_period(
    query_params: QueryParams = Depends(get_query_params),
    current_account: Account = Depends(get_current_user),
    operation_services: OperationsServices = Depends(),
):
    return operation_services.get_operations(
        current_account,
        query_params,
    )


@router.get(
    '/report',
    description=description,
    tags=['Operations'],
)
def get_operations_report(
    query_params: QueryParams = Depends(get_query_params),
    current_account: Account = Depends(get_current_user),
    operation_services: OperationsServices = Depends(),
):
    return operation_services.get_report(current_account, query_params)
