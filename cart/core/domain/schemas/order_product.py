from typing import Type
from pydantic import BaseModel, Field

from cart.core.domain.schemas.order import Order
from cart.core.domain.schemas.product import Product


class OrderProduct(BaseModel):
    order: Type['Order'] = Field(...)
    product: Type['Product'] = Field(...)
