from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_auth_service
from app.schemas.users import UserCreate, UserRead
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
):
    try:
        return auth_service.register(user_data)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )