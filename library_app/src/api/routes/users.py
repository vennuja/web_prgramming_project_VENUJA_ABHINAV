from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any

from ...db.session import get_db
from ...models.users import User as UserModel
from ..schemas.users import User, UserCreate, UserUpdate
from ...repositories.users import UserRepository
from ...services.users import UserService
from ..dependencies import get_current_admin_user

router = APIRouter()


@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_admin_user)
) -> Any:
    repository = UserRepository(UserModel, db)
    service = UserService(repository)
    users = service.get_multi(skip=skip, limit=limit)
    return users


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user=Depends(get_current_admin_user)
) -> Any:
    repository = UserRepository(UserModel, db)
    service = UserService(repository)
    try:
        user = service.create(user_in)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=User)
def read_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user=Depends(get_current_admin_user)
) -> Any:
    repository = UserRepository(UserModel, db)
    service = UserService(repository)
    user = service.get(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.put("/{id}", response_model=User)
def update_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    user_in: UserUpdate,
    current_user=Depends(get_current_admin_user)
) -> Any:
    repository = UserRepository(UserModel, db)
    service = UserService(repository)
    user = service.get(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    try:
        updated_user = service.update(user, user_in)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{id}", response_model=User)
def delete_user(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user=Depends(get_current_admin_user)
) -> Any:
    repository = UserRepository(UserModel, db)
    service = UserService(repository)
    user = service.get(id=id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    deleted_user = service.remove(id=id)
    return deleted_user
