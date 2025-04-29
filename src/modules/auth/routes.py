from fastapi import APIRouter, Request

from src.modules.auth import request_schemas as requests, response_schemas as responses
from src.modules.auth.controller import AuthControllerDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=responses.TokenResponse)
async def login(
        login_data: requests.LoginRequest,
        controller: AuthControllerDep,
) -> responses.TokenResponse:
    return await controller.login(login_data)


@router.post("/logout")
async def logout(
        request: Request,
        controller: AuthControllerDep,
) -> responses.LogoutResponse:
    return await controller.logout(request)


@router.post("/refresh", response_model=responses.TokenResponse)
async def refresh(
        refresh_data: requests.RefreshRequest,
        controller: AuthControllerDep,
) -> responses.TokenResponse:
    return await controller.refresh(refresh_data)
