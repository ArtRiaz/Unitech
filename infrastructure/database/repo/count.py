from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from infrastructure.database.model import Count, User
from infrastructure.database.repo.base import BaseRepo


class CountRepo(BaseRepo):
    async def get_or_create_register(
            self,
            adress_type_object: str,
            electric_time: str = None,
            tarif: str = None,
            crowl: str = None,
            type_crowl: str = None,
            type_system: str = None,
            power_station: str = None,
            acamulator: str = None,
            phone: str = None,
            email: str = None,

    ):
        insert_stmt = (
            insert(Count)
            .values(
                adress_type_object=adress_type_object,
                electric_time=electric_time,
                tarif=tarif,
                crowl=crowl,
                type_crowl=type_crowl,
                type_system=type_system,
                power_station=power_station,
                acamulator=acamulator,
                phone=phone,
                email=email,
            )
            .returning(Count)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()
