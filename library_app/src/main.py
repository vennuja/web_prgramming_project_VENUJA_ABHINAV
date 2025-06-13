from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .api.routes import api_router
from .models import base, books, users, loans  # Importer les modèles pour Alembic

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}
