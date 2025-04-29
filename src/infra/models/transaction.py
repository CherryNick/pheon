from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base import Base
from src.infra.models.enum.base import IntEnum
from src.infra.models.mixins import CreatedAtServerDefaultMixin, IDIntegerMixin

if TYPE_CHECKING:
    from src.infra.models.user import User
else:
    User = "User"


class TransactionType(IntEnum):
    DEPOSIT = 1
    BUY_POINTS = 2
    TRANSFER = 3
    WITHDRAW_TO_SYSTEM = 4


class Transaction(Base, IDIntegerMixin, CreatedAtServerDefaultMixin):
    __tablename__ = "transaction"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    receiver_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True)

    transaction_type: Mapped[TransactionType] = mapped_column(IntEnum(TransactionType))

    amount: Mapped[float] = mapped_column(Numeric(precision=12, scale=2))

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
    receiver: Mapped["User"] = relationship("User", foreign_keys=[receiver_id])
