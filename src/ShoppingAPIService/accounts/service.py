from fastapi import Depends
from passlib.hash import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound, IntegrityError

from ..database import Session, get_session
from ..config import Settings, get_settings
from ..exseptions import EntiyDoesNotExistError, EntityConflictError
from .auth import create_token
from .models import Account
from .schemas import AccountSingUp, AccountSingIn, Token
from .schemas import Account as AccountSchema


class AccountService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        settings: Settings = Depends(get_settings),
    ):
        self.session = session
        self.settings = settings

    def create_account(self, account_singup: AccountSingUp) -> Account:
        account = Account(
            email=account_singup.email,
            username=account_singup.username,
            password=pbkdf2_sha256.hash(account_singup.password)
        )
        self.session.add(account)
        try:
            self.session.commit()
            return account
        except IntegrityError:
            raise EntityConflictError

    def create_token_for_account(self, account_token: Account) -> Token:
        account = AccountSchema(
            id=account_token.id,
            username=account_token.username,
        )
        return Token(
            access_token=create_token(account),
            token_type="bearer",
        )

    def get_account_by_username(self, account_singin: AccountSingIn) -> Account:
        try:
            account = self.session.execute(
                select(Account)
                .where(Account.username == account_singin.username)
            ).scalar_one()
        except NoResultFound:
            raise EntiyDoesNotExistError
        if not pbkdf2_sha256.verify(account_singin.password, account.password):
            raise EntiyDoesNotExistError
        return account
