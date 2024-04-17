from pydantic import BaseModel, Field
from fastapi import Body


class ProductId(BaseModel):
    product_id: int = Field(Body(alias="product-id", embed=True))
