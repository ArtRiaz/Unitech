from typing import Optional

from sqlalchemy import String, LargeBinary
from sqlalchemy import text, BIGINT, Boolean, true, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Register(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    name: Mapped[Optional[str]] = mapped_column(String(128))
    contact: Mapped[str] = mapped_column(String(128))
    pdf_file: Mapped[Optional[bytes]] = mapped_column(LargeBinary, nullable=True)
    comment: Mapped[str] = mapped_column(String(128))

    def __repr__(self):
        return f"<User {self.name} {self.contact} {self.comment} >"
