from typing import Optional

from sqlalchemy import String
from sqlalchemy import text, BIGINT, Boolean, true, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Register(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    name: Mapped[Optional[str]] = mapped_column(String(128))
    profession: Mapped[str] = mapped_column(String(100))
    contact: Mapped[str] = mapped_column(String(128))
    age: Mapped[str] = mapped_column(String(100))
    expirience: Mapped[str] = mapped_column(String(100))

    def __repr__(self):
        return f"<User {self.name} {self.age} {self.contact} {self.profession} {self.expirience} >"
