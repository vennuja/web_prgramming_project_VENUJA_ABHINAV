import pytest
from sqlalchemy.orm import Session

from src.models.categories import Category
from src.repositories.categories import CategoryRepository

def test_create_category(db_session: Session):
    """
    Test category creation
    """
    repository = CategoryRepository(Category, db_session)
    
    category_data = {
        "name": "Science Fiction",
        "description": "Sci-fi books"
    }
    
    category = repository.create(obj_in=category_data)
    
    assert category.id is not None
    assert category.name == "Science Fiction"
    assert category.description == "Sci-fi books"

def test_get_category_by_name(db_session: Session):
    """
    Test retrieving category by name
    """
    repository = CategoryRepository(Category, db_session)
    
    # Create test category
    repository.create(obj_in={
        "name": "Fantasy",
        "description": "Fantasy genre books"
    })
    
    # Test retrieval
    category = repository.get_by_name(name="Fantasy")
    assert category is not None
    assert category.description == "Fantasy genre books"

def test_update_category(db_session: Session):
    """
    Test category update
    """
    repository = CategoryRepository(Category, db_session)
    
    # Create initial category
    category = repository.create(obj_in={
        "name": "Technology",
        "description": "Tech books"
    })
    
    # Update category
    updated_category = repository.update(
        db_obj=category,
        obj_in={"description": "Technology and programming books"}
    )
    
    assert updated_category.name == "Technology"
    assert updated_category.description == "Technology and programming books"