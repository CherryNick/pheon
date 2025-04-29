import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status

from src.extensions.access_token import AccessToken
from src.extensions.dependencies import ConfigDep, GetDBSessionDep
from src.infra.repositories.sqlalchemy.uow import SqlAlchemyRepositories
from src.modules.base.service import SqlAlchemyService
from src.utils import pwd_context


@dataclass(slots=True)
class AuthService(SqlAlchemyService):
    @staticmethod
    def _hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _create_access_token(self, user_id: int, expires_delta: timedelta) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub": str(user_id),
            "iat": now,
            "exp": now + expires_delta,
        }
        token = jwt.encode(payload, self.config.jwt.secret, algorithm=self.config.jwt.algorithm)
        return token

    def _create_refresh_token(self, user_id: int, expires_delta: timedelta) -> str:
        return self._create_access_token(user_id, expires_delta)

    def _decode_access_token(self, token: str) -> AccessToken:
        payload = jwt.decode(token, self.config.jwt.secret, algorithms=[self.config.jwt.algorithm])
        return AccessToken(**payload)

    def _decode_refresh_token(self, token: str) -> AccessToken:
        try:
            return self._decode_access_token(token)
        except jwt.DecodeError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token") from e

    async def login(self, username: str, password: str) -> dict:
        user = await self.repos.user.get_by_username(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        if not pwd_context.verify(password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        access_token = self._create_access_token(
            user_id=user.id,
            expires_delta=timedelta(minutes=self.config.jwt.access_token_expire_minutes),
        )
        refresh_token = self._create_refresh_token(
            user_id=user.id,
            expires_delta=timedelta(minutes=self.config.jwt.refresh_token_expire_minutes),
        )
        self.repos.user.set_user_refresh_token(
            user=user,
            token_hash=self._hash_token(refresh_token),
            expire_minutes=self.config.jwt.refresh_token_expire_minutes,
        )
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    async def refresh_tokens(self, refresh_token: str) -> dict:
        payload = self._decode_refresh_token(refresh_token)
        user_id = payload.sub

        user = await self.repos.user.get_with_refresh_token(user_id)
        if not user or not user.refresh_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        if self._hash_token(refresh_token) != user.refresh_token.token_hash:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

        access_token = self._create_access_token(
            user_id=int(user_id),
            expires_delta=timedelta(minutes=self.config.jwt.access_token_expire_minutes),
        )
        new_refresh_token = self._create_refresh_token(
            user_id=int(user_id),
            expires_delta=timedelta(minutes=self.config.jwt.refresh_token_expire_minutes),
        )

        self.repos.user.set_user_refresh_token(
            user=user,
            token_hash=self._hash_token(new_refresh_token),
            expire_minutes=self.config.jwt.refresh_token_expire_minutes,
        )

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        }

    async def revoke_token(self, token: str) -> None:
        payload = self._decode_access_token(token)
        user_id = payload.sub
        user = await self.repos.user.get_with_refresh_token(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        self.repos.user.remove_refresh_token(user)


def get_service(
        config: ConfigDep,
        session: GetDBSessionDep,
) -> AuthService:
    repos = SqlAlchemyRepositories(session=session)
    return AuthService(config, repos=repos)


AuthServiceDep = Annotated[AuthService, Depends(get_service)]
