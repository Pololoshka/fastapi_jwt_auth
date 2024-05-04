from collections.abc import Callable
from types import TracebackType
from typing import Self

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db.repos import UserRepo


class SqlAlchemyUnitOfWork:
    session: AsyncSession

    def __init__(self, session_factory: Callable[[], AsyncSession]):
        self.session_factory = session_factory

    async def __aenter__(self) -> None:
        self.session = self.session_factory()
        self.users = UserRepo(session=self.session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    @classmethod
    def from_url(cls, url: URL) -> Self:
        return cls(session_factory=async_sessionmaker(bind=create_async_engine(url=url)))
