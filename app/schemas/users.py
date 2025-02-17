from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.items import UserItemOut

class UserCreate(BaseModel):
    username: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")

class UserRequest(BaseModel):
    username: str = Field(..., description="Логин")

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    coins: int
    inventory: Optional[List[UserItemOut]] = None

class Token(BaseModel):
    access_token: str

class TransferCreate(BaseModel):
    to_user_id: int
    amount: int

class Transfer(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    from_user_id: int
    to_user_id: int
    amount: int