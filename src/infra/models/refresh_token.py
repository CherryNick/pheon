from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infra.models.base import Base
from src.infra.models.mixins import CreatedAtServerDefaultMixin, IDIntegerMixin

if TYPE_CHECKING:
    from src.infra.models.user import User
else:
    User = "User"


class RefreshToken(Base, IDIntegerMixin, CreatedAtServerDefaultMixin):
    __tablename__ = "refresh_token"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    token_hash: Mapped[str]
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user: Mapped[User] = relationship(User, back_populates="refresh_token")
