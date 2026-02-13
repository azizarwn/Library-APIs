from datetime import date, timedelta

# Database connection
from pathlib import Path

from sqlmodel import Session, create_engine, select

from app.models.models import Book, BorrowingRecords, Member

# Get the project root directory (parent of app folder)
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "database.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, echo=True)


def create_tables():
    """Tables are created via Alembic migrations"""
    # Skip table creation - Alembic handles this
    pass


def seed_books(session: Session):
    """Seed books data"""
    books_data = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "published_year": 1925,
            "isbn": "978-0-7432-7356-5",
        },
        {"title": "To Kill a Mockingbird", "author": "Harper Lee", "published_year": 1960, "isbn": "978-0-06-112008-4"},
        {"title": "1984", "author": "George Orwell", "published_year": 1949, "isbn": "978-0-452-28423-4"},
        {"title": "Pride and Prejudice", "author": "Jane Austen", "published_year": 1813, "isbn": "978-0-14-143951-8"},
        {
            "title": "The Catcher in the Rye",
            "author": "J.D. Salinger",
            "published_year": 1951,
            "isbn": "978-0-316-76948-0",
        },
        {
            "title": "Harry Potter and the Philosopher's Stone",
            "author": "J.K. Rowling",
            "published_year": 1997,
            "isbn": "978-0-7475-3269-9",
        },
        {"title": "The Hobbit", "author": "J.R.R. Tolkien", "published_year": 1937, "isbn": "978-0-618-00221-3"},
        {"title": "Fahrenheit 451", "author": "Ray Bradbury", "published_year": 1953, "isbn": "978-1-4516-7331-9"},
        {"title": "The Da Vinci Code", "author": "Dan Brown", "published_year": 2003, "isbn": "978-0-385-50420-1"},
        {"title": "The Alchemist", "author": "Paulo Coelho", "published_year": 1988, "isbn": "978-0-06-112241-5"},
    ]

    books = []
    for book_data in books_data:
        book = Book(**book_data)
        session.add(book)
        books.append(book)

    session.commit()
    print(f"✅ Seeded {len(books)} books")
    return books


def seed_members(session: Session):
    """Seed members data"""
    members_data = [
        {"name": "Alice Johnson", "email": "alice.johnson@email.com"},
        {"name": "Bob Smith", "email": "bob.smith@email.com"},
        {"name": "Charlie Brown", "email": "charlie.brown@email.com"},
        {"name": "Diana Prince", "email": "diana.prince@email.com"},
        {"name": "Ethan Hunt", "email": "ethan.hunt@email.com"},
        {"name": "Fiona Green", "email": "fiona.green@email.com"},
        {"name": "George Wilson", "email": "george.wilson@email.com"},
        {"name": "Hannah Lee", "email": "hannah.lee@email.com"},
    ]

    members = []
    for member_data in members_data:
        member = Member(**member_data)
        session.add(member)
        members.append(member)

    session.commit()
    print(f"✅ Seeded {len(members)} members")
    return members


def seed_borrowing_records(session: Session, books: list[Book], members: list[Member]):
    """Seed borrowing records data"""

    # Define some realistic borrowing scenarios
    borrowing_data = [
        # Currently borrowed books (no return date)
        {
            "book_id": books[0].id,
            "member_id": members[0].id,
            "member_name": members[0].name,
            "borrow_date": date.today() - timedelta(days=5),
            "return_date": None,
        },
        {
            "book_id": books[2].id,
            "member_id": members[1].id,
            "member_name": members[1].name,
            "borrow_date": date.today() - timedelta(days=10),
            "return_date": None,
        },
        {
            "book_id": books[5].id,
            "member_id": members[3].id,
            "member_name": members[3].name,
            "borrow_date": date.today() - timedelta(days=3),
            "return_date": None,
        },
        # Recently returned books
        {
            "book_id": books[1].id,
            "member_id": members[0].id,
            "member_name": members[0].name,
            "borrow_date": date.today() - timedelta(days=30),
            "return_date": date.today() - timedelta(days=2),
        },
        {
            "book_id": books[3].id,
            "member_id": members[2].id,
            "member_name": members[2].name,
            "borrow_date": date.today() - timedelta(days=25),
            "return_date": date.today() - timedelta(days=5),
        },
        {
            "book_id": books[4].id,
            "member_id": members[4].id,
            "member_name": members[4].name,
            "borrow_date": date.today() - timedelta(days=20),
            "return_date": date.today() - timedelta(days=6),
        },
        # Older borrowing history
        {
            "book_id": books[6].id,
            "member_id": members[5].id,
            "member_name": members[5].name,
            "borrow_date": date.today() - timedelta(days=60),
            "return_date": date.today() - timedelta(days=45),
        },
        {
            "book_id": books[7].id,
            "member_id": members[6].id,
            "member_name": members[6].name,
            "borrow_date": date.today() - timedelta(days=90),
            "return_date": date.today() - timedelta(days=75),
        },
        {
            "book_id": books[8].id,
            "member_id": members[7].id,
            "member_name": members[7].name,
            "borrow_date": date.today() - timedelta(days=45),
            "return_date": date.today() - timedelta(days=30),
        },
        # Same book borrowed multiple times by different members
        {
            "book_id": books[0].id,
            "member_id": members[2].id,
            "member_name": members[2].name,
            "borrow_date": date.today() - timedelta(days=70),
            "return_date": date.today() - timedelta(days=55),
        },
        # Same member borrowing multiple books
        {
            "book_id": books[9].id,
            "member_id": members[1].id,
            "member_name": members[1].name,
            "borrow_date": date.today() - timedelta(days=35),
            "return_date": date.today() - timedelta(days=20),
        },
    ]

    records = []
    for record_data in borrowing_data:
        record = BorrowingRecords(**record_data)
        session.add(record)
        records.append(record)

    session.commit()
    print(f"✅ Seeded {len(records)} borrowing records")
    return records


def main():
    """Main seeder function"""
    print("🌱 Starting database seeding...\n")

    # Note: Make sure you've run Alembic migrations first!
    print("⚠️  Make sure you've run: alembic upgrade head\n")

    # Create session
    with Session(engine) as session:
        # Check if data already exists
        existing_books = session.exec(select(Book)).first()
        if existing_books:
            print("⚠️  Database already contains data. Skipping seeding.")
            print("💡 Run 'alembic downgrade base' then 'alembic upgrade head' to reset.")
            return

        # Seed data
        books = seed_books(session)
        members = seed_members(session)
        borrowing_records = seed_borrowing_records(session, books, members)

        print("\n✨ Database seeding completed successfully!")
        print(f"📚 Total: {len(books)} books, {len(members)} members, {len(borrowing_records)} borrowing records")


if __name__ == "__main__":
    main()
