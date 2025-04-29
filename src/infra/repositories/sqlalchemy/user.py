from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.infra.models.refresh_token import RefreshToken
from src.infra.models.user import User
from src.infra.repositories.base.sqlalchemy import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def create_user(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        self.session.add(user)
        return user

    async def get_by_username(self, username: str, load_refresh_token: bool = False) -> User | None:
        stmt = select(User).where(User.username == username)
        if load_refresh_token:
            stmt = stmt.options(
            joinedload(User.refresh_token),
        )
        return (await self.session.execute(stmt)).scalar()

    async def get_with_refresh_token(self, user_id: int) -> User | None:
        stmt = select(User).options(
            joinedload(User.refresh_token),
        ).where(User.id == user_id)
        return (await self.session.execute(stmt)).scalar()

    def set_user_refresh_token(self, user: User, token_hash: str, expire_minutes: int) -> None:
        user.refresh_token = RefreshToken(
            token_hash=token_hash, expires_at=datetime.now() + timedelta(minutes=expire_minutes),
        )
        self.session.add(user.refresh_token)

    @staticmethod
    def remove_refresh_token(user: User) -> None:
        user.refresh_token = None
