from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, tasks

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="0.1.0")

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/")
def root():
    return {"message": "Task Management API running"}
