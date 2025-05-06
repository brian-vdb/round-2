# app.py

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from api.auth import router as auth_router
from db.setup import init_db
from db.handlers.user import get_user_by_email, create_user
from schemas.user import UserCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
  """
  Initialize DB and ensure a root user exists before the app starts.
  """
  # 1) Create tables if they don’t exist
  init_db()

  # 2) Read credentials
  root_email: str | None = os.getenv("ROOT_EMAIL")
  root_password: str | None = os.getenv("ROOT_PASSWORD")
  if not root_email or not root_password:
    raise RuntimeError("Please set ROOT_EMAIL and ROOT_PASSWORD in your .env")

  # 3) Ensure root user
  if get_user_by_email(root_email) is None:
    root_in = UserCreate(
      username="root",
      email=root_email,
      password=root_password
    )
    create_user(root_in)
    print(f"[app.py]: Created root user: {root_email}")

  # Let FastAPI continue to startup
  yield

# Attach the lifespan
app = FastAPI(lifespan=lifespan)

# Mount your auth routes
app.include_router(auth_router, prefix="/auth")


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="127.0.0.1", port=8000)
