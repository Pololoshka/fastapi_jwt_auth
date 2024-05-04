import asyncio
import json
from datetime import date
from pathlib import Path
from typing import Any

from passlib.context import CryptContext
from sqlalchemy import delete

from src.db.models import SalaryStatus, User
from src.db.uow import SqlAlchemyUnitOfWork
from src.settings import DBSettings

file = Path(__file__).parent / "data.json"


async def main(db_settings: DBSettings) -> None:
    data = json.loads(file.read_text())

    uow = SqlAlchemyUnitOfWork.from_url(url=db_settings.db_url)
    async with uow:
        await delete_data(data=data, uow=uow)
        await uow.session.flush()
        load_data(data=data, uow=uow)


def load_data(data: list[dict[str, Any]], uow: SqlAlchemyUnitOfWork) -> None:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    for raw_user in data:
        user = User(
            username=raw_user["username"],
            first_name=raw_user["first_name"],
            last_name=raw_user["last_name"],
            hashed_password=pwd_context.hash(raw_user["password"]),
            salary=SalaryStatus(
                username=raw_user["salary"]["username"],
                amount=raw_user["salary"]["amount"],
                currency=raw_user["salary"]["currency"],
                next_increases_at=date.fromisoformat(raw_user["salary"]["next_increases_at"]),
            ),
        )
        uow.session.add(user)


async def delete_data(data: list[dict[str, Any]], uow: SqlAlchemyUnitOfWork) -> None:
    usernames = {user["username"] for user in data}
    await uow.session.execute(delete(User).where(User.username.in_(usernames)))


if __name__ == "__main__":
    asyncio.run(main(DBSettings()))
