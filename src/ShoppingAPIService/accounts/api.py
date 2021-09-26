from fastapi import APIRouter
from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm

from ..exseptions import EntityConflictError, EntiyDoesNotExistError
from .service import AccountService
from .schemas import AccountSingIn, AccountSingUp, Token

router = APIRouter()


def initialize_app(app: FastAPI):
    app.include_router(router)


@router.post(
    '/signup',
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    tags=['Accounts'],
)
def create_account(
    account_create: AccountSingUp,
    account_service: AccountService = Depends(),
):
    try:
        account = account_service.create_account(account_create)
    except EntityConflictError:
        raise HTTPException(status.HTTP_409_CONFLICT)
    return account_service.create_token_for_account(account)


@router.post('/signin', response_model=Token, tags=['Accounts'])
def authenticate_account(
    account_service: AccountService = Depends(),
    credentials: OAuth2PasswordRequestForm = Depends(),
):
    account_singin = AccountSingIn(
        username=credentials.username,
        password=credentials.password,
    )
    try:
        account = account_service.get_account_by_username(account_singin)
    except EntiyDoesNotExistError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    return account_service.create_token_for_account(account)
