from app.core.auth import hash_password,verify_password,create_access_token
from app.models.users import User
from app.repositories.users import UserRepository
from app.schemas.users import UserCreate,UserLogin,Token

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
    
    def login(self, data: UserLogin) -> Token:
        if data.username:
            user, sub = self.user_repository.get_by_username(data.username), data.username
            err = "No account registered with this username"
        elif data.email:
            user, sub = self.user_repository.get_by_email(data.email), data.email
            err = "No account registered with this email"
        else:
            raise ValueError("Username or email required")

        if not user:
            raise ValueError(err)

        if not verify_password(data.password, user.hashed_password):
            raise ValueError("Incorrect password")

        return create_access_token({"sub": sub})


            







        