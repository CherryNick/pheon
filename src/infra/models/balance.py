from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base import Base
from src.infra.models.mixins import CreatedAtServerDefaultMixin, IDIntegerMixin, UpdatedAtServerDefaultMixin

if TYPE_CHECKING:
    from src.infra.models.user import User
else:
    User = "User"


class Balance(Base, IDIntegerMixin, CreatedAtServerDefaultMixin, UpdatedAtServerDefaultMixin):
    __tablename__ = "balance"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)

    funds: Mapped[float] = mapped_column(Numeric(precision=12, scale=2), default=0)
    points: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship("User", back_populates="balance")
