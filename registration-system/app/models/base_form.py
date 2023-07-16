from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class BaseFormMixin:
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
