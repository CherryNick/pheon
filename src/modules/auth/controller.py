from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status

from src.extensions.dependencies import ConfigDep
from src.modules.auth import request_schemas as requests, response_schemas as responses
from src.modules.auth.service import AuthService, AuthServiceDep
from src.modules.base.controller import BaseController


@dataclass(slots=True)
class AuthController(BaseController):
    service: AuthService

    @staticmethod
    def _get_token_from_request(request: Request) -> str:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing or invalid Authorization header",
            )
        token_str = auth_header.removeprefix("Bearer ").strip()
        return token_str

    async def login(self, data: requests.LoginRequest) -> responses.TokenResponse:
        result = await self.service.login(data.username, data.password)
        return responses.TokenResponse(**result)

    async def logout(self, request: Request) -> responses.LogoutResponse:
        token = self._get_token_from_request(request)
        await self.service.revoke_token(token)
        return responses.LogoutResponse()

    async def refresh(self, data: requests.RefreshRequest) -> responses.TokenResponse:
        result = await self.service.refresh_tokens(data.refresh_token)
        return responses.TokenResponse(**result)


async def get_controller(config: ConfigDep, service: AuthServiceDep) -> AuthController:
    return AuthController(config, service)

AuthControllerDep = Annotated[AuthController, Depends(get_controller)]
