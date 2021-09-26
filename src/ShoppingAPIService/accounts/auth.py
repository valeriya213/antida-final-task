from datetime import datetime, timedelta
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

from ..config import settings
from .schemas import Account


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='signin')


def create_token(account: Account) -> str:
    now = datetime.utcnow()
    return jwt.encode(
        {
            'sub': str(account.id),
            'exp': now + timedelta(seconds=settings.jwt_access_livetime),
            'iat': now,
            'nbf': now,
            'account': {
                'id': str(account.id),
                'username': account.username,
            }},
        'secret',
        algorithm='HS256',
    )


def get_current_user(token: str = Depends(oauth2_scheme)) -> Account:
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Unauthorized user',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        token_data = jwt.decode(
            token,
            'secret',
            algorithms=['HS256'],
        )
    except ExpiredSignatureError:
        raise credentials_exeption
    except JWTError:
        raise credentials_exeption

    if 'account' not in token_data:
        raise credentials_exeption
    return Account(**token_data['account'])
