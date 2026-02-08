# src/main.py
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from src.config.database import engine
from src.config.logging import setup_logging
from src.api import auth, tasks  # make sure tasks exists and its router is correct
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    # Create DB tables (only for simple dev setups)
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title="Todo API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
# include tasks router only if defined
try:
    app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])
except Exception:
    # If tasks router isn't ready, keep server running for auth testing
    pass

@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")
