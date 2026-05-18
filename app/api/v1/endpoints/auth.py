from fastapi import APIRouter, Depends

from app.api.deps import get_auth_service
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from app.utils.rate_limit import check_login_rate_limit

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
    _: None = Depends(check_login_rate_limit),
) -> TokenResponse:
    token = auth_service.login(payload.username, payload.password)
    return TokenResponse(access_token=token)
