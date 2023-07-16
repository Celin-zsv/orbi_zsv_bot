import datetime

from sqlalchemy.orm import Mapped

from app.core.db import Base
from app.models.base_form import BaseFormMixin


class BirthdayForm(BaseFormMixin, Base):
    date: Mapped[datetime.date]
