# api/auth.py

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from internal.auth import create_access_token, get_current_user
from db.handlers.user import login_user
from db.models.user import User
from schemas.user import UserRead

router = APIRouter()

class LoginData(BaseModel):
  username: str
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

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

  # Build payload from every ORM column except password
  payload = {
    col.name: getattr(orm_user, col.name)
    for col in User.__table__.columns
    if col.name != "password"
  }

  access_token = create_access_token(payload)
  return {"access_token": access_token, "token_type": "bearer"}

@router.get(
  "/validate",
  response_model=UserRead,
  summary="Validate a token and return the current user",
)
async def validate(current_user: User = Depends(get_current_user)) -> UserRead:
  # FastAPI will convert the returned ORM User into UserRead automatically
  return current_user
