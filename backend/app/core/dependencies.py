from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt

from app.core.database import get_session
from app.repositories.users import UserRepository
from app.services.auth import AuthService

from app.core.auth import SECRET_KEY, ALGORITHM
from app.models.users import User

from app.repositories.notes import NoteRepository
from app.services.notes import NoteService

from app.services.embeddings import Embedder, get_embedder

def get_user_repository(
    session: Session = Depends(get_session),
) -> UserRepository:
    return UserRepository(session)

def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository)

# Notes
def get_note_repository(
    session: Session = Depends(get_session)
) -> NoteRepository:
    return NoteRepository(session)

def get_note_service(
    note_repository: NoteRepository = Depends(get_note_repository),
    embedder: Embedder = Depends(get_embedder),
) -> NoteService:
    return NoteService(note_repository, embedder)

# Token

bearer_scheme = HTTPBearer()

def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), 
        user_repository: UserRepository = Depends(get_user_repository),
    ):

    token = credentials.credentials
    # print("Token:", token)

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get("sub")
        # print("Decoded payload:", payload)
        if id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    user = user_repository.get_by_id(int(id))
    # print("Retrieved user:", user.email)
    if user is None:
        raise credentials_exception
    return user