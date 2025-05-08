# data/db/setup.py

import os
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, Session as SessionType

# Database URL – override via env var
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./storage.db")

# Create engine
engine: Engine = create_engine(
  DATABASE_URL,
  connect_args={"check_same_thread": False}
  if DATABASE_URL.startswith("sqlite")
  else {},
)

# Session factory
SessionLocal: sessionmaker = sessionmaker(
  autocommit=False,
  autoflush=False,
  bind=engine,
)

# Base class for models
Base: DeclarativeMeta = declarative_base()


def init_db() -> None:
  """
  Import all modules here that might define models so
  that they will be registered properly on the metadata.
  Then create all tables.
  """
  import data.db.models.user
  Base.metadata.create_all(bind=engine)


@contextmanager
def LocalSession() -> Iterator[SessionType]:
  """
  Provide the session.
  """
  db: SessionType = SessionLocal()
  try:
    yield db
  finally:
    db.close()
