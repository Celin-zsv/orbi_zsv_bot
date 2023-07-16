from sqlalchemy.orm import Mapped

from app.core.db import Base
from app.models.base_form import BaseFormMixin


class AnotherForm(BaseFormMixin, Base):
    help: Mapped[str]
