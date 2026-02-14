from pydantic import BaseModel


class MemberRequest(BaseModel):
    name: str
    email: str


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class MemberDetailResponse(BaseModel):
    id: int
    name: str
    email: str
    borrowing_history: list[dict] = []
    currently_borrowed_books: list[dict] = []

    class Config:
        from_attributes = True
