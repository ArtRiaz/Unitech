from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from infrastructure.database.model import Register, User
from infrastructure.database.repo.base import BaseRepo


class RegisterRepo(BaseRepo):
    async def get_or_create_register(
            self,
            name: str,
            contact: str,
            comment: str,
            pdf_file: Optional[bytes] = None,

    ):
        insert_stmt = (
            insert(Register)
            .values(
                name=name,
                contact=contact,
                comment=comment,
                pdf_file=pdf_file,
            )
            .returning(Register)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()


class SelectRepo(BaseRepo):
    async def select_all_registers(self):
        stmt = select(Register)
        result = await self.session.execute(stmt)
        return result.scalars().all()
