from typing import List
from pydantic import BaseModel, ConfigDict, Field

class ItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    type: str
    amount: int