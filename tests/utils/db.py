from asyncio import AbstractEventLoop
from collections.abc import AsyncGenerator, Generator
from functools import partial
from typing import Any

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
)

from src.db.uow import SqlAlchemyUnitOfWork
from src.settings import DBSettings


@pytest.fixture(scope="session")
def db_url() -> URL:
    settings = DBSettings(_env_file=".env.tests")
    return settings.db_url


@pytest.fixture(scope="session")
def alembic_config(db_url: URL) -> Config:
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url.render_as_string(hide_password=False))
    return alembic_cfg


@pytest.fixture(scope="session")
async def engine(
    db_url: "URL", alembic_config: Config, event_loop: Generator[AbstractEventLoop, Any, None]
) -> AsyncGenerator[AsyncConnection, None]:
    engine = create_async_engine(db_url)
    connection = await engine.connect()

    await connection.run_sync(partial(execute_upgrade, alembic_config))

    yield connection

    await connection.run_sync(partial(execute_downgrade, alembic_config))
    await connection.close()
    await engine.dispose()


def execute_upgrade(cfg: Config, connection: AsyncConnection) -> None:
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


def execute_downgrade(cfg: Config, connection: AsyncConnection) -> None:
    cfg.attributes["connection"] = connection
    command.downgrade(cfg, "base")


@pytest.fixture()
async def session(engine: AsyncConnection) -> AsyncGenerator[AsyncSession, None]:
    transaction = engine.begin()
    await transaction.start()
    async with AsyncSession(bind=engine, expire_on_commit=False) as session:
        yield session

    await transaction.rollback()
    await transaction.close()


@pytest.fixture()
async def uow(session: AsyncSession) -> AsyncGenerator[SqlAlchemyUnitOfWork, None]:
    uow = SqlAlchemyUnitOfWork(session_factory=lambda: session)  # type: ignore
    async with uow:
        yield uow
