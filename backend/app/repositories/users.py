from sqlalchemy.orm import Session

from app.models.users import User

class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> User | None:
        return (
            self.session.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_username(self, username: str) -> User | None:
        return (
            self.session.query(User)
            .filter(User.username == username)
            .first()
        )
    

    def add(self, user: User) -> User:
        self.session.add(user)
        self.session.flush()

        return user

    def commit(self):
        self.session.commit()