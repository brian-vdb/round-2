# db/handlers/user.py

from typing import Optional
from passlib.context import CryptContext

from db.setup import LocalSession
from db.models.user import User
from schemas.user import UserRead, UserCreate

# Password‐hashing context
pwd_context: CryptContext = CryptContext(
  schemes=["argon2", "bcrypt_sha256"],
  default="argon2",
  deprecated="auto",
)


def get_user_by_email(email: str) -> Optional[UserRead]:
  """
  Retrieve a user by email, returned as a Pydantic UserRead.
  """
  with LocalSession() as db:
    user: Optional[User] = db.query(User).filter(User.email == email).first()
    if user is None:
      return None
    return UserRead.model_validate(user)


def create_user(user_in: UserCreate) -> User:
  """
  Create a new user (hashes password internally).
  """
  with LocalSession() as db:
    hashed_password: str = pwd_context.hash(user_in.password)
    db_user: User = User(
      username=user_in.username,
      email=user_in.email,
      password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_password(user_id: int, new_password: str) -> User:
  """
  Update a user's password (hashes new password internally).
  """
  with LocalSession() as db:
    user: Optional[User] = db.query(User).filter(User.id == user_id).first()
    if user is None:
      raise ValueError(f"User with id {user_id} not found")
    user.password = pwd_context.hash(new_password)
    db.commit()
    db.refresh(user)
    return user
  
  
def login_user(username: str, password: str) -> Optional[User]:
  """
  Authenticate a user by username & raw password.
  Returns the full ORM User on success, or None if invalid.
  """
  with LocalSession() as db:
    user: Optional[User] = (
      db.query(User)
        .filter(User.username == username)
        .first()
    )
    if user is None:
      return None

    if not pwd_context.verify(password, user.password):
      return None

    return user
