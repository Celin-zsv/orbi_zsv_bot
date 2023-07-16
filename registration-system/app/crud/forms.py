from app.crud.base import CRUDBase
from app.models.another_form import AnotherForm
from app.models.birthday_form import BirthdayForm
from app.models.run_form import RunForm

another_crud = CRUDBase(AnotherForm)
birthday_crud = CRUDBase(BirthdayForm)
run_crud = CRUDBase(RunForm)
