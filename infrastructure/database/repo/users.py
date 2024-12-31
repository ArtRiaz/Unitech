from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select

from infrastructure.database.model.user import User
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        user_id: int,
        full_name: str,
        language: str,
        username: Optional[str] = None,
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param user_id: The user's ID.
        :param full_name: The user's full name.
        :param language: The user's language.
        :param username: The user's username. It's an optional parameter.
        :return: User object, None if there was an error while making a transaction.

        Args:
            referral_id:
            referral_id: referral_id (Optional[int]): The user's referral ID.
        """

        insert_stmt = (
            insert(User)
            .values(
                user_id=user_id,
                username=username,
                full_name=full_name,
                language=language,
            )
            .on_conflict_do_update(
                index_elements=[User.user_id],
                set_=dict(
                    username=username,
                    full_name=full_name,
                ),
            )
            .returning(User)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()


class CountSelectUser(BaseRepo):
    async def count_users(self):
        """
        Selects all users (user_id and username) from the database and returns them as a list of tuples.
        """
        stmt = select(User.user_id, User.username)  # Выбираем user_id и username
        result = await self.session.execute(stmt)
        return [(row.user_id, row.username) for row in result]

