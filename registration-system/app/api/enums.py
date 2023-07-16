from enum import Enum

from app.crud.forms import another_crud, birthday_crud, run_crud
from app.schemas.forms import AnotherFormCreate, BirthdayFormCreate, RunFormCreate


class Form(str, Enum):
    def __new__(cls, title: str, crud, schema):
        obj = str.__new__(cls, title)
        obj._value_ = title
        obj.crud = crud
        obj.schema = schema
        return obj

    ANOTHER_FORM = ("another", another_crud, AnotherFormCreate)
    BIRTHDAY_FORM = ("birthday", birthday_crud, BirthdayFormCreate)
    RUN_FORM = ("run", run_crud, RunFormCreate)
