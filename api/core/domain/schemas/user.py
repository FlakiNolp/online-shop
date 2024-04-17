from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional, List

from api.core.domain.schemas.order import Order


class User(BaseModel):
    email: EmailStr = Field(...)
    hashed_password: str = Field(...)
    role: Literal["Admin", "User"] = Field(...)
