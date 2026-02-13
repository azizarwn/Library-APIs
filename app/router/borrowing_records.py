from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Book, BorrowingRecords, Member
from app.schema.borrowing_record import BorrowingRecordRequest, BorrowingRecordResponse

borrow_router = APIRouter(prefix="/borrowing_records", tags=["Borrowing Records"])


@borrow_router.get(path="/", response_model=list[BorrowingRecordResponse])
def get_borrowing_records(db: Session = Depends(get_db)):
    query = select(BorrowingRecords)
    books = db.exec(query).all()

    return books


@borrow_router.post(path="/")
def create_borrowing_record(body: BorrowingRecordRequest, db: Session = Depends(get_db)):
    # 1. Check if book exists
    book = db.get(Book, body.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 2. Check if book is available
    if not book.is_available:
        raise HTTPException(status_code=400, detail="Book is currently borrowed")

    # 3. Check if member exists
    member = db.get(Member, body.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # 4. Create borrowing record
    new_record = BorrowingRecords(
        book_id=body.book_id,
        member_id=body.member_id,
        member_name=member.name,  # ✅ Get member name from member object
        borrow_date=date.today(),  # ✅ Set today's date automatically
        return_date=body.return_date,  # Can be None
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {"success": True, "data": new_record, "message": "Borrowing record created successfully"}
