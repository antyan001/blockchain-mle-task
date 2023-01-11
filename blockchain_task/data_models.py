from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    city: str
    state: Optional[str]
    country: str
    postCode: str


class User(BaseModel):
    id: str
    address: Address


class ReportFigures(BaseModel):
    users_cnt: int
    us_users_cnt: int
    non_us_users_cnt: int
