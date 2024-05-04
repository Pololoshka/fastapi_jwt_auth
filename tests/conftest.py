import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
from dotenv import load_dotenv
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from passlib.context import CryptContext

from src.db.uow import SqlAlchemyUnitOfWork
from src.settings import AuthenticationSettings, DBSettings

pytest_plugins = ["pytest_asyncio", "tests.utils.db", "tests.utils.models"]

load_dotenv(".env.tests", override=True)


@pytest.fixture(scope="session")
def event_loop(
    request: type[pytest.FixtureRequest],
) -> Generator[asyncio.AbstractEventLoop, Any, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def app(event_loop: Generator[asyncio.AbstractEventLoop, Any, None]) -> FastAPI:
    from src.main import app as _app

    return _app


@pytest.fixture()
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://localhost") as client:  # type: ignore
        yield client


@pytest.fixture(autouse=True)
def _override_dependency(
    app: AsyncClient,
    uow: SqlAlchemyUnitOfWork,
) -> None:
    from src.db.connect import uow as uow_

    app.dependency_overrides[uow_] = lambda: uow  # type: ignore


@pytest.fixture()
def db_settings() -> DBSettings:
    return DBSettings()


@pytest.fixture()
def auth_settings() -> AuthenticationSettings:
    return AuthenticationSettings()


@pytest.fixture()
def pwd_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")
