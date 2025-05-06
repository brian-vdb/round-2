# backend/api/auth.py

import os
from datetime import datetime, timezone
from typing import Optional

from jose import JWTError, jwt
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from db.setup import LocalSession
from db.handlers.user import login_user
from db.models.user import User
from schemas.user import UserRead

router = APIRouter()

# --- Schemas --------------------------------------------------

class LoginData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


# --- JWT settings --------------------------------------------

SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable must be set")

ALGORITHM: str = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_payload: dict) -> str:
    """
    Create a signed JWT containing the minimal user payload.
    """
    to_encode = user_payload.copy()
    to_encode["iat"] = datetime.now(timezone.utc)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- Routes ---------------------------------------------------

@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate and get a JWT containing the full user",
)
async def login(data: LoginData) -> dict[str, str]:
    orm_user = login_user(data.username, data.password)
    if not orm_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    payload = {
        col.name: getattr(orm_user, col.name)
        for col in User.__table__.columns
        if col.name != "password"
    }

    access_token = create_access_token(payload)
    return {"access_token": access_token, "token_type": "bearer"}


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
        user_id: int | None = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    with LocalSession() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user


@router.get(
    "/validate",
    response_model=UserRead,
    summary="Validate a token and return the current user",
)
async def validate(current_user: User = Depends(get_current_user)) -> UserRead:
    # FastAPI will convert the returned ORMUser into UserRead automatically
    return current_user
