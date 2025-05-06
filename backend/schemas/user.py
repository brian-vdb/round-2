# schemas/user.py

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
  username: str
  email: EmailStr
  password: str

class UserRead(BaseModel):
  id: int
  username: str
  email: EmailStr

  # Pydantic v2: enable 'from_attributes' globally
  model_config = {
    "from_attributes": True
  }
