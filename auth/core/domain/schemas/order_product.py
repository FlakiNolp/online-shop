from typing import Type
from pydantic import BaseModel, Field

from auth.core.domain.schemas.order import Order
from auth.core.domain.schemas.product import Product


class OrderProduct(BaseModel):
    order: Type['Order'] = Field(...)
    product: Type['Product'] = Field(...)
