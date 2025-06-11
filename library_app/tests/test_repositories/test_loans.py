import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.models.loans import Loan
from src.models.books import Book
from src.models.users import User
from src.repositories.loans import LoanRepository
from src.repositories.books import BookRepository
from src.repositories.users import UserRepository

@pytest.fixture
def setup_loan_data(db_session: Session):
    """Fixture to set up test data for loan tests"""
    # Create test book
    book_repo = BookRepository(Book, db_session)
    book = book_repo.create(obj_in={
        "title": "Loan Test Book",
        "author": "Test Author",
        "isbn": "1112223334444",
        "publication_year": 2020,
        "quantity": 5
    })
    
    # Create test user
    user_repo = UserRepository(User, db_session)
    user = user_repo.create(obj_in={
        "email": "borrower@example.com",
        "hashed_password": "pass123",
        "full_name": "Test Borrower"
    })
    
    return book, user

def test_create_loan(db_session: Session, setup_loan_data):
    """
    Test loan creation
    """
    book, user = setup_loan_data
    repository = LoanRepository(Loan, db_session)
    
    loan_data = {
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow(),
        "due_date": datetime.utcnow() + timedelta(days=14)
    }
    
    loan = repository.create(obj_in=loan_data)
    
    assert loan.id is not None
    assert loan.book_id == book.id
    assert loan.user_id == user.id
    assert loan.return_date is None

def test_get_active_loans(db_session: Session, setup_loan_data):
    """
    Test retrieval of active loans
    """
    book, user = setup_loan_data
    repository = LoanRepository(Loan, db_session)
    
    # Create active loan
    active_loan = repository.create(obj_in={
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow(),
        "due_date": datetime.utcnow() + timedelta(days=14)
    })
    
    # Create returned loan
    returned_loan = repository.create(obj_in={
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow() - timedelta(days=30),
        "due_date": datetime.utcnow() - timedelta(days=16),
        "return_date": datetime.utcnow() - timedelta(days=15)
    })
    
    active_loans = repository.get_active_loans()
    
    assert len(active_loans) == 1
    assert active_loans[0].id == active_loan.id

def test_get_overdue_loans(db_session: Session, setup_loan_data):
    """
    Test retrieval of overdue loans
    """
    book, user = setup_loan_data
    repository = LoanRepository(Loan, db_session)
    
    # Create overdue loan
    overdue_loan = repository.create(obj_in={
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow() - timedelta(days=30),
        "due_date": datetime.utcnow() - timedelta(days=1),
        "return_date": None
    })
    
    # Create non-overdue loan
    current_loan = repository.create(obj_in={
        "user_id": user.id,
        "book_id": book.id,
        "loan_date": datetime.utcnow(),
        "due_date": datetime.utcnow() + timedelta(days=14),
        "return_date": None
    })
    
    overdue_loans = repository.get_overdue_loans()
    
    assert len(overdue_loans) == 1
    assert overdue_loans[0].id == overdue_loan.id