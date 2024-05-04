from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from src import models as dm
from src.db.connect import uow
from src.db.uow import SqlAlchemyUnitOfWork
from src.dependencies import auth_settings, pwd_context
from src.handlers import AuthenticateHandler
from src.settings import AuthenticationSettings

router = APIRouter(prefix="/api/login", tags=["Login"])


@router.post("/", response_model=dm.Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    uow: Annotated[SqlAlchemyUnitOfWork, Depends(uow)],
    settings: Annotated[AuthenticationSettings, Depends(auth_settings)],
    context: Annotated[CryptContext, Depends(pwd_context)],
) -> dm.Token:
    handler = AuthenticateHandler(auth_settings=settings, pwd_context=context)

    user = await uow.users.get_slim(username=form_data.username)
    if not user or not handler.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = handler.create_access_token(
        data=dm.TokenData(username=user.username).model_dump(by_alias=True)
    )
    return dm.Token(access_token=access_token)
