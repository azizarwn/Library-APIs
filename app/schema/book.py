from pydantic import BaseModel


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str
    published_year: int
    is_available: bool

    class Config:
        from_attributes = True


class BookRequest(BaseModel):
    title: str
    author: str
    isbn: str
    published_year: int
