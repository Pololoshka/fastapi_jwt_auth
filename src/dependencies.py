from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from src import models as dm
from src.settings import AuthenticationSettings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def auth_settings() -> AuthenticationSettings:
    return AuthenticationSettings()


def pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def check_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[AuthenticationSettings, Depends(auth_settings)],
) -> dm.TokenData:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return dm.TokenData.model_validate(payload)
    except (JWTError, ValidationError) as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from err
