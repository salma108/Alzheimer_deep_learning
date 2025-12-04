# src/api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .auth_router import router as auth_router
from .analysis import router as analysis_router
from .history import router as history_router

# Création des tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Alzheimer MRI Assistant API")

# CORS pour ton front Vite (5173)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static : rapports PDF
app.mount("/static/reports", StaticFiles(directory="reports"), name="reports")

# Routers
app.include_router(auth_router)
app.include_router(analysis_router)
app.include_router(history_router)
