from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends

from src.db.uow import SqlAlchemyUnitOfWork
from src.settings import DBSettings


def db_settings() -> DBSettings:
    return DBSettings()


def uow_engine(settings: Annotated[DBSettings, Depends(db_settings)]) -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork.from_url(url=settings.db_url)


async def uow(
    uow_engine: Annotated[SqlAlchemyUnitOfWork, Depends(uow_engine)],
) -> AsyncGenerator[SqlAlchemyUnitOfWork, None]:
    async with uow_engine:
        yield uow_engine
