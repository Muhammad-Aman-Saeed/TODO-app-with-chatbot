from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .routes.tasks import router as tasks
from .routes.auth import router as auth
from .routes.chat import router as chat
from .db import engine
from sqlmodel import SQLModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Import models here to ensure they're registered with SQLModel metadata before creating tables
    from .models import Task, Conversation, Message  # noqa: F401
    # Startup logic - create database tables
    SQLModel.metadata.create_all(bind=engine)
    yield
    # Shutdown logic can go here

# Create FastAPI app with lifespan
app = FastAPI(
    title="Hackathon Todo Backend API",
    description="Secure task management API with JWT authentication",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS - allow origins for both development and production
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001"
]

# Add production domain if available
prod_origin = os.getenv("PRODUCTION_ORIGIN")
if prod_origin:
    allowed_origins.append(prod_origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers for JWT
    expose_headers=["Authorization"]
)

# Include task router with prefix
app.include_router(tasks, prefix="/api", tags=["tasks"])

# Include auth router with prefix
app.include_router(auth, prefix="/api", tags=["auth"])

# Include chat router with prefix
app.include_router(chat, prefix="/api", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon Todo Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)