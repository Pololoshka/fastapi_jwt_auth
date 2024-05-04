from datetime import date
from typing import Optional

from sqlalchemy import DATE, Float, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(DeclarativeBase, MappedAsDataclass): ...


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(100))

    salary: Mapped[Optional["SalaryStatus"]] = relationship(lazy="noload")


class SalaryStatus(Base):
    __tablename__ = "salary_statuses"

    username: Mapped[str] = mapped_column(
        ForeignKey(column="users.username", ondelete="CASCADE"), primary_key=True
    )
    amount: Mapped[float] = mapped_column(Float)
    currency: Mapped[str] = mapped_column(server_default="RUB")
    next_increases_at: Mapped[date] = mapped_column(DATE())
