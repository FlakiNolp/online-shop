from pydantic import BaseModel, Field
from fastapi import Query, Path


class GetProduct(BaseModel):
    category: str | None = Field(Query(alias='category', default=None), min_length=1, max_length=50)
    price_from: float | None = Field(Query(alias='price-from', default=None), ge=0)
    price_to: float | None = Field(Query(alias='price-to', default=None), ge=0)
