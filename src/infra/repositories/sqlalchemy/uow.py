from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.repositories.sqlalchemy.user import UserRepository


class SqlAlchemyRepositories:
    """Unit Of Work pattern"""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.user = UserRepository(session)
