import pytest
from sqlalchemy.orm import Session

from src.models.users import User
from src.repositories.users import UserRepository

def test_create_user(db_session: Session):
    """
    Test user creation
    """
    repository = UserRepository(User, db_session)
    
    user_data = {
        "email": "test@example.com",
        "hashed_password": "hashedpass123",
        "full_name": "Test User",
        "is_active": True,
        "is_admin": False
    }
    
    user = repository.create(obj_in=user_data)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.is_active is True

def test_get_user_by_email(db_session: Session):
    """
    Test retrieving user by email
    """
    repository = UserRepository(User, db_session)
    
    # Create test user
    repository.create(obj_in={
        "email": "unique@example.com",
        "hashed_password": "hashedpass123",
        "full_name": "Unique User"
    })
    
    # Test retrieval
    user = repository.get_by_email(email="unique@example.com")
    assert user is not None
    assert user.full_name == "Unique User"

def test_update_user(db_session: Session):
    """
    Test user update functionality
    """
    repository = UserRepository(User, db_session)
    
    # Create initial user
    user = repository.create(obj_in={
        "email": "update@example.com",
        "hashed_password": "oldpass",
        "full_name": "Original Name"
    })
    
    # Update user
    updated_user = repository.update(
        db_obj=user,
        obj_in={"full_name": "Updated Name", "is_active": False}
    )
    
    assert updated_user.full_name == "Updated Name"
    assert updated_user.is_active is False