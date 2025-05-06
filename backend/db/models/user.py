# db/models/user.py

from sqlalchemy import Column, Integer, String
from db.setup import Base

class User(Base):
  __tablename__ = 'users'

  id = Column(Integer, primary_key=True, index=True, autoincrement=True)
  username = Column(String, unique=True, index=True, nullable=False)
  email = Column(String, unique=True, index=True, nullable=False)
  password = Column(String, nullable=False)
