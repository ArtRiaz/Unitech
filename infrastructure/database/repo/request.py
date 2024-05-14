from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repo.users import UserRepo, CountSelectUser
from infrastructure.database.setup import create_engine
from infrastructure.database.repo.register import RegisterRepo, SelectRepo


@dataclass
class RequestsRepo:
    """
    Repository for handling database operations. This class holds all the repositories for the database models.

    You can add more repositories as properties to this class, so they will be easily accessible.
    """

    session: AsyncSession

    @property
    def users(self) -> UserRepo:
        """
        The User repository sessions are required to manage user operations.
        """
        return UserRepo(self.session)

    @property
    def register(self) -> RegisterRepo:
        """
        The Register repository sessions are required to manage register operations.
        """
        return RegisterRepo(self.session)

    @property
    def select(self) -> SelectRepo:
        """
        The Register repository sessions are required to manage register operations.
        """
        return SelectRepo(self.session)

    @property
    def count_users(self) -> CountSelectUser:
        """
        The Register repository sessions are required to manage register operations.
        """
        return CountSelectUser(self.session)
