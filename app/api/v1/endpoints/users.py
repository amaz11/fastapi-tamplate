from fastapi import APIRouter, Depends, status

from app.api.deps import get_current_username, get_user_service
from app.models.user import User
from app.schemas.user import UserCreate, UserPublic, UserRead
from app.services.user_service import UserService
from app.utils.response import success_response

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def list_users(user_service: UserService = Depends(get_user_service)) -> list[UserRead]:
    return user_service.list_users()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> dict:
    user = user_service.create_user(payload)
    return success_response(UserPublic.model_validate(user))


@router.get("/me", response_model=UserPublic)
def read_me(
    current_username: str = Depends(get_current_username),
    user_service: UserService = Depends(get_user_service),
) -> UserPublic:
    user = next(user for user in user_service.list_users() if user.username == current_username)
    return UserPublic.model_validate(user)
