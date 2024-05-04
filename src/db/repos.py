from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.db.models import User


class UserRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_slim(self, username: str) -> User | None:
        user = await self.session.scalar(select(User).where(User.username == username))
        return user

    async def get(self, username: str) -> User | None:
        user = await self.session.scalar(
            select(User).options(joinedload(User.salary)).where(User.username == username)
        )
        return user
