from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base import Base
from src.infra.models.mixins import CreatedAtServerDefaultMixin, IDIntegerMixin, UpdatedAtServerDefaultMixin

if TYPE_CHECKING:
    from src.infra.models.balance import Balance
    from src.infra.models.refresh_token import RefreshToken
else:
    RefreshToken = "RefreshToken"
    Balance = "Balance"


class User(Base, IDIntegerMixin, CreatedAtServerDefaultMixin, UpdatedAtServerDefaultMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()

    refresh_token: Mapped[RefreshToken] = relationship(
        RefreshToken, uselist=False, cascade="all, delete-orphan", back_populates="user",
    )
    balance: Mapped["Balance"] = relationship(
        "Balance", back_populates="user", uselist=False, cascade="all, delete-orphan",
    )
