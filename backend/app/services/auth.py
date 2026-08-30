from app.core.auth import hash_password
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import UserCreate

class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register(self, data: UserCreate) -> User:

        existing_user = self.user_repository.get_by_email(data.email)

        if existing_user:
            raise ValueError("email already registered")

        existing_user = self.user_repository.get_by_username(data.username)

        if existing_user:
            raise ValueError("username already taken")

        hashed_password = hash_password(data.password)

        user = User(
            username=data.username,
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password=hashed_password,
        )

        created_user = self.user_repository.add(user)
        self.user_repository.commit()

        return created_user