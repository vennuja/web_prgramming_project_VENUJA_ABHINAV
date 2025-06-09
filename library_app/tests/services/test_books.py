import pytest
from sqlalchemy.orm import Session

from src.models.books import Book
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.api.schemas.books import BookCreate, BookUpdate


def test_create_book(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="1984",
        author="George Orwell",
        isbn="9780451524935",
        publication_year=1949,
        description="Dystopian novel",
        quantity=10
    )

    book = service.create(obj_in=book_in)

    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.isbn == "9780451524935"
    assert book.quantity == 10


def test_get_by_isbn(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Animal Farm",
        author="George Orwell",
        isbn="9780451526342",
        publication_year=1945,
        description="Political satire",
        quantity=5
    )

    service.create(obj_in=book_in)
    book = service.get_by_isbn(isbn="9780451526342")

    assert book is not None
    assert book.title == "Animal Farm"
