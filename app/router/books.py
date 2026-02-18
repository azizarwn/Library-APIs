from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select

from app.models.engine import get_db
from app.models.models import Book
from app.schema.book import BookRequest, BookResponse

books_router = APIRouter(prefix="/books", tags=["Books"])


@books_router.get(path="/", response_model=list[BookResponse])
def get_books(is_available: bool | None = None, db: Session = Depends(get_db)):
    query = select(Book)
    books = db.exec(query).all()

    if is_available is not None:
        books = [book for book in books if book.is_available == is_available]

    return books


@books_router.get(path="/{id}", response_model=BookResponse)
def get_book_by_id(id: int, db: Session = Depends(get_db)):
    book = db.get(Book, id)
    return book


@books_router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def create_book(body: BookRequest, db: Session = Depends(get_db)):
    new_book = Book(**body.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)  # Get the ID and computed properties
    return new_book
