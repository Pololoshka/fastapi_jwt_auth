from datetime import date

from pydantic import BaseModel, ConfigDict, Field, alias_generators


class BaseCamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel,
        populate_by_name=True,
    )


class Token(BaseCamelCaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseCamelCaseModel):
    username: str = Field(alias="sub")


class SalaryStatus(BaseCamelCaseModel):
    model_config = ConfigDict(from_attributes=True)
    amount: float
    currency: str
    next_increases_at: date


class User(BaseCamelCaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    first_name: str
    last_name: str
    salary: SalaryStatus
