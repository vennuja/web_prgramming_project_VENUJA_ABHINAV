from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..models.users import User
from ..repositories.users import UserRepository
from ..services.users import UserService
from ..api.schemas.token import TokenPayload
from ..utils.security import ALGORITHM
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actuel à partir du token JWT.
    """
    try:
        print(f"🔐 Raw token: {token}")  # Debug line

        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        print(f"Decoded payload: {payload}")  # Debug line

        # DEBUG: If `sub` is a string, convert it to int
        if isinstance(payload.get("sub"), str):
            payload["sub"] = int(payload["sub"])

        token_data = TokenPayload(**payload)
        print(f"Token data parsed: {token_data}")  # Debug line

    except (JWTError, ValidationError) as e:
        print(f"JWT or validation error: {e}")  # Debug line
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Impossible de valider les informations d'identification",
        )

    repository = UserRepository(User, db)
    service = UserService(repository)
    user = service.get(id=token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur non trouvé",
        )
    return user



def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Dépendance pour obtenir l'utilisateur actif actuel.
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Utilisateur inactif",
        )
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Dépendance pour obtenir l'utilisateur administrateur actuel.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Privilèges insuffisants",
        )
    return current_user
