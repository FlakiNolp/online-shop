from pydantic import BaseModel, Field


class Image(BaseModel):
    name: str = Field(ge=75, le=3)
