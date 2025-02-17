from typing import List
from pydantic import BaseModel, ConfigDict, Field




class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)