from datetime import UTC, date, datetime, timedelta

import pytest
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import SalaryStatus, User
from src.settings import AuthenticationSettings


@pytest.fixture()
async def user(session: AsyncSession, pwd_context: CryptContext) -> User:
    user = User(
        username="@ivani",
        first_name="Ivan",
        last_name="Ivanov",
        hashed_password=pwd_context.hash("12345"),
        salary=None,
    )
    session.add(user)
    await session.flush()
    return user


@pytest.fixture()
async def salary(session: AsyncSession, user: User) -> SalaryStatus:
    user.salary = SalaryStatus(
        username=user.username,
        currency="RUB",
        amount=15000.00,
        next_increases_at=date(year=2024, month=10, day=10),
    )
    session.add(user.salary)
    await session.flush()
    return user.salary


@pytest.fixture()
def token(user: User, auth_settings: AuthenticationSettings) -> str:
    data = {"sub": user.username}
    expire = datetime.now(UTC) + timedelta(minutes=auth_settings.access_token_expire_minutes)
    data.update({"exp": expire})  # type: ignore
    return jwt.encode(data, key=auth_settings.secret_key, algorithm=auth_settings.algorithm)  # type: ignore
