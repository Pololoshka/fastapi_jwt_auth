from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from src import models as dm
from src.db.connect import uow
from src.db.uow import SqlAlchemyUnitOfWork
from src.dependencies import check_token

router = APIRouter(prefix="/api/salary", tags=["Salary"])


@router.get("/", response_model=dm.User)
async def get_user(
    token: Annotated[dm.TokenData, Depends(check_token)],
    uow: Annotated[SqlAlchemyUnitOfWork, Depends(uow)],
) -> dm.User:
    user = await uow.users.get(username=token.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return dm.User.model_validate(user)
