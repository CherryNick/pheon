from typing import Sequence

from sqlalchemy import select

from infra.models.transaction import Transaction, TransactionType
from infra.repositories.base.sqlalchemy import SQLAlchemyRepository


class TransactionRepository(SQLAlchemyRepository[Transaction]):
    async def create(
        self,
        user_id: int,
        type_: TransactionType,
        amount: float,
        receiver_id: int | None = None,
    ) -> Transaction:
        transaction = Transaction(
            user_id=user_id,
            transaction_type=type_,
            amount=amount,
            receiver_id=receiver_id,
        )
        self.session.add(transaction)
        await self.session.flush()
        await self.session.refresh(transaction)
        return transaction

    async def list_user_transactions(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Transaction]:
        stmt = (
            select(Transaction)
            .where(Transaction.user_id == user_id)
            .order_by(Transaction.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
