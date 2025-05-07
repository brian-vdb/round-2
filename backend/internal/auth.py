# internal/auth.py

from datetime import datetime, timezone
import os
from typing import Optional

from jose import JWTError, jwt
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from db.setup import LocalSession
from db.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
if not SECRET_KEY:
  raise RuntimeError("SECRET_KEY environment variable must be set")

ALGORITHM: str = "HS256"


def create_access_token(user_payload: dict) -> str:
  """
  Create a signed JWT containing the minimal user payload.
  """
  to_encode = user_payload.copy()
  to_encode["iat"] = datetime.now(timezone.utc)
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
  """
  Dependency that decodes the JWT, looks up the ORM User, and returns it.
  """
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id: Optional[int] = payload.get("id")
    if user_id is None:
      raise credentials_exception
  except JWTError:
    raise credentials_exception

  with LocalSession() as db:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
      raise credentials_exception
    return user
  