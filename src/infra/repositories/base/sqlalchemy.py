from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.repositories.base.protocol import RepositoryProtocol, T


class SQLAlchemyRepository(RepositoryProtocol[T]):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self.session = session
        self.model = model

    async def get_by_id(self, id_: int) -> T | None:
        stmt = select(self.model).where(self.model.id == id_)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar()

    async def add(self, obj: T) -> None:
        self.session.add(obj)

    async def delete(self, obj: T) -> None:
        await self.session.delete(obj)
