from pydantic import BaseModel


class Account(BaseModel):
    id: int
    username: str


class AccountSingUp(BaseModel):
    email: str
    username: str
    password: str


class AccountSingIn(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
