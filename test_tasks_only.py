from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import just the tasks route
from backend.routes.tasks import router as tasks

app = FastAPI(title="Test Server with Tasks Only")

# Configure CORS for localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include task router with prefix
app.include_router(tasks, prefix="/api", tags=["tasks"])

@app.get("/")
def read_root():
    return {"message": "Test server with tasks only running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)