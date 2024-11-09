from typing import List

from pydantic import BaseModel, Field, UUID4


class BookCreate(BaseModel):
    title: str = Field(max_length=64)
    authors: List[UUID4]
    publication_year: int = Field(ge=0, lt=2025)  # calc when run app, save to constant
    pages: int = Field(gt=0)
    genre: str = Field(max_length=64)


class Book(BookCreate):
    uid: UUID4

    class Config:
        from_attributes = True
