from httpx import AsyncClient

from src.db.models import User


async def test_login_user(client: AsyncClient, user: User) -> None:
    response = await client.post(
        url="/api/login/",
        data={"username": user.username, "password": "12345"},
    )

    assert response.status_code == 200
    assert "accessToken" in response.json()
    assert response.json()["tokenType"] == "bearer"


async def test_login_user__error_incorrect_password(client: AsyncClient, user: User) -> None:
    response = await client.post(
        url="/api/login/",
        data={"username": user.username, "password": "234234"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_login_user__error_incorrect_username(client: AsyncClient) -> None:
    response = await client.post(
        url="/api/login/",
        data={"username": "user", "password": "12345"},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


async def test_login_user__error_validaton(client: AsyncClient) -> None:
    response = await client.post(
        url="/api/login/",
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "username"],
                "msg": "Field required",
                "input": None,
            },
            {
                "type": "missing",
                "loc": ["body", "password"],
                "msg": "Field required",
                "input": None,
            },
        ]
    }
