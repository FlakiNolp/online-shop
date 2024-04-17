from typing import Type
from pydantic import BaseModel, Field

from api.core.domain.schemas.order import Order
from api.core.domain.schemas.product import Product


class OrderProduct(BaseModel):
    order: Type['Order'] = Field(...)
    product: Type['Product'] = Field(...)
