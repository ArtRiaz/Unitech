from typing import Optional

from sqlalchemy import String, LargeBinary
from sqlalchemy import text, BIGINT, Boolean, true, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TimestampMixin, TableNameMixin, int_pk


class Count(Base, TimestampMixin, TableNameMixin):
    id: Mapped[int_pk]
    adress_type_object: Mapped[Optional[str]] = mapped_column(String(128))
    electric_time: Mapped[str] = mapped_column(String(128), nullable=True)
    tarif: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    crowl: Mapped[str] = mapped_column(String(128), nullable=True)
    type_crowl: Mapped[str] = mapped_column(String(128), nullable=True)
    type_system: Mapped[str] = mapped_column(String(128), nullable=True)
    power_station: Mapped[str] = mapped_column(String(128), nullable=True)
    acamulator: Mapped[str] = mapped_column(String(128), nullable=True)
    phone: Mapped[str] = mapped_column(String(128), nullable=True)
    email: Mapped[str] = mapped_column(String(128), nullable=True)

    def __repr__(self):
        return f"<User {self.name} {self.contact} {self.comment} >"