from pydantic import BaseModel, Field
from typing import Optional, List


class Category(BaseModel):
    name: str = Field(ge=100, le=3)
