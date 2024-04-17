from pydantic import BaseModel, Field
from typing import Optional, List

from auth.core.domain.schemas.category import Category
from auth.core.domain.schemas.image import Image


class Product(BaseModel):
    name: str = Field(ge=100, le=3)
    description: Optional[str] = Field(ge=350)
    price: float = Field(...)
    quantity: int = Field(...)
    category: Optional['Category'] = Field(...)
    images: Optional[List['Image']] = Field(...)
