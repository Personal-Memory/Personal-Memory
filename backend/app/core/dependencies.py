from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_session
from app.repositories.users import UserRepository
from app.services.auth import AuthService

def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)