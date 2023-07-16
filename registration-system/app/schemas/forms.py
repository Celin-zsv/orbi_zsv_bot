import datetime

from pydantic import BaseModel, EmailStr, Extra, Field


class FormBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr

    class Config:
        extra = Extra.forbid


class AnotherFormCreate(FormBase):
    help: str = Field(..., min_length=1)


class BirthdayFormCreate(FormBase):
    date: datetime.date


class RunFormCreate(FormBase):
    pass
