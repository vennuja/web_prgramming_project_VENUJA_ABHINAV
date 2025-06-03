from fastapi import APIRouter

from .books import router as books_router
from .users import router as users_router
from .loans import router as loans_router
from .auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(books_router, prefix="/books", tags=["books"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(loans_router, prefix="/loans", tags=["loans"])
