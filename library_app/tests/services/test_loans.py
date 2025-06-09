import pytest
from sqlalchemy.orm import Session
from datetime import timedelta, datetime

from src.models.loans import Loan
from src.models.books import Book
from src.models.users import User
from src.repositories.loans import LoanRepository
from src.repositories.books import BookRepository
from src.repositories.users import UserRepository
from src.services.loans import LoanService
from src.api.schemas.books import BookCreate
from src.api.schemas.users import UserCreate


def test_create_and_return_loan(db_session: Session):
    user_repo = UserRepository(User, db_session)
    book_repo = BookRepository(Book, db_session)
    loan_repo = LoanRepository(Loan, db_session)
    service = LoanService(loan_repo, book_repo, user_repo)

    # Create user and book
    user = user_repo.create(UserCreate(
        email="loan@example.com",
        password="pass123",
        full_name="Loan Tester"
    ))
    book = book_repo.create(BookCreate(
        title="Test Book",
        author="Author",
        isbn="1234567890123",
        publication_year=2020,
        description="Test book",
        quantity=5
    ))

    # Create loan
    loan = service.create_loan(user_id=user.id, book_id=book.id, loan_period_days=7)
    assert loan.user_id == user.id
    assert loan.book_id == book.id
    assert loan.return_date is None

    # Return loan
    returned = service.return_loan(loan_id=loan.id)
    assert returned.return_date is not None
    assert returned.id == loan.id


def test_overdue_and_active_loans(db_session: Session):
    user_repo = UserRepository(User, db_session)
    book_repo = BookRepository(Book, db_session)
    loan_repo = LoanRepository(Loan, db_session)
    service = LoanService(loan_repo, book_repo, user_repo)

    # Create user and book
    user = user_repo.create(UserCreate(
        email="overdue@example.com",
        password="pass123",
        full_name="Overdue Tester"
    ))
    book = book_repo.create(BookCreate(
        title="Book Overdue",
        author="Author",
        isbn="3213213213210",
        publication_year=2022,
        description="Test overdue",
        quantity=2
    ))

    # Create overdue loan
    loan = service.create_loan(user_id=user.id, book_id=book.id, loan_period_days=-1)

    active_loans = service.get_active_loans()
    overdue_loans = service.get_overdue_loans()

    assert loan in active_loans
    assert loan in overdue_loans
