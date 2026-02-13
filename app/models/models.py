from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  # int | None => auto increment
    title: str
    author: str
    published_year: int
    isbn: str
    borrowing_records: list["BorrowingRecords"] = Relationship(back_populates="book")

    @property
    def is_available(self) -> bool:
        # Book is available if:
        # - It has no borrowing records at all, OR
        # - All borrowing records have a return_date (meaning the book was returned)

        # Book is NOT available if:
        # - There's any borrowing record with return_date = None (currently borrowed)

        if not self.borrowing_records:
            return True  # No borrowing history = available

        # Check if any record has no return date (currently borrowed)
        return not any(record.return_date is None for record in self.borrowing_records)


class Member(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: str
    borrowing_records: list["BorrowingRecords"] = Relationship(back_populates="member")


class BorrowingRecords(SQLModel, table=True):
    borrow_id: int | None = Field(default=None, primary_key=True)
    book_id: int = Field(foreign_key="book.id")
    member_id: int = Field(foreign_key="member.id")
    borrow_date: date
    return_date: date | None = None
    book: Book = Relationship(back_populates="borrowing_records")
    member: Member = Relationship(back_populates="borrowing_records")
