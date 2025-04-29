from sqlalchemy import select

from infra.models.balance import Balance
from infra.repositories.base.sqlalchemy import SQLAlchemyRepository


class BalanceRepository(SQLAlchemyRepository[Balance]):
    async def get_by_user_id(self, user_id: int) -> Balance | None:
        stmt = select(Balance).where(Balance.user_id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_funds(self, balance: Balance, amount: float) -> None:
        balance.funds += amount
        self.session.add(balance)

    async def subtract_funds(self, balance: Balance, amount: float) -> None:
        balance.funds -= amount
        self.session.add(balance)

    async def add_points(self, balance: Balance, points: int) -> None:
        balance.points += points
        self.session.add(balance)

    async def save(self) -> None:
        await self.session.commit()
