from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import just the auth route
from backend.routes.auth import router as auth

app = FastAPI(title="Test Server with Auth Only")

# Configure CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include auth router with prefix
app.include_router(auth, prefix="/api", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Test server with auth only running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)