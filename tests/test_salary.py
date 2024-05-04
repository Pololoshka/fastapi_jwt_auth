from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import SalaryStatus, User


async def test_get_salary(client: AsyncClient, token: str, salary: SalaryStatus) -> None:
    response = await client.get(url="/api/salary/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json() == {
        "username": "@ivani",
        "firstName": "Ivan",
        "lastName": "Ivanov",
        "salary": {"amount": 15000.0, "currency": "RUB", "nextIncreasesAt": "2024-10-10"},
    }


async def test_get_salary__error_token(client: AsyncClient) -> None:
    response = await client.get(url="/api/salary/", headers={"Authorization": "Bearer fdgf"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}


async def test_get_salary__error_user(
    client: AsyncClient, session: AsyncSession, token: str, user: User
) -> None:
    await session.delete(user)
    await session.flush()

    response = await client.get(url="/api/salary/", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}
