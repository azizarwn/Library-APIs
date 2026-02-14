from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Book, BorrowingRecords, Member
from app.schema.borrowing_record import BorrowingRecordRequest, BorrowingRecordResponse, UpdateBorrowingRecordRequest

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
        borrow_date=date.today(),  # ✅ Set today's date automatically
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return {"success": True, "data": new_record, "message": "Borrowing record created successfully"}


@borrow_router.patch(path="/{borrow_id}")
def update_borrowing_record(borrow_id: int, body: UpdateBorrowingRecordRequest, db: Session = Depends(get_db)):
    # 1. Check if borrowing record exists
    record = db.get(BorrowingRecords, borrow_id)
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Borrowing record not found")

    # 2. Check if already returned
    if record.return_date is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book has already been returned")

    # 3. Validate return date is not before borrow date
    if body.return_date and body.return_date < record.borrow_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Return date cannot be before borrow date")

    # 4. Update the record
    record.return_date = body.return_date

    db.add(record)
    db.commit()
    db.refresh(record)

    return {"success": True, "data": record, "message": "Book returned successfully"}
