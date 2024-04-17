import datetime
from pydantic import BaseModel, Field


class Order(BaseModel):
    datetime_of_order: datetime.datetime = Field(...)
