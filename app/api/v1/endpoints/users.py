from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_current_user, get_user_service
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserCreate, UserPublic, UserRead
from app.services.user_service import UserService
from app.utils.pagination import PaginatedResponse, build_pagination_meta
from app.utils.response import success_response

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=PaginatedResponse[UserRead])
def list_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(None, ge=1, le=settings.max_page_size),
    user_service: UserService = Depends(get_user_service),
) -> PaginatedResponse[UserRead]:
    size = page_size or settings.default_page_size
    users, total = user_service.list_users(page=page, page_size=size)
    return PaginatedResponse(
        items=[UserRead.model_validate(user) for user in users],
        meta=build_pagination_meta(page=page, page_size=size, total=total),
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    user = user_service.create_user(payload)
    return success_response(UserPublic.model_validate(user))


@router.get("/me", response_model=UserPublic)
def read_me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.model_validate(current_user)
