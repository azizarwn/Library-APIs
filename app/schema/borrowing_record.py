from datetime import date

from pydantic import BaseModel


class BorrowingRecordRequest(BaseModel):
    book_id: int
    member_id: int


class BorrowingRecordResponse(BaseModel):
    borrow_id: int
    book_id: int
    member_id: int
    borrow_date: date
    return_date: date | None = None

    class Config:
        from_attributes = True


class UpdateBorrowingRecordRequest(BaseModel):
    return_date: date | None = None
