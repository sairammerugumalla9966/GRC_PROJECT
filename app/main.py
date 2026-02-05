from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, tasks, users
from app.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Management API", version="0.1.0")

# Include routers
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)

# ----------------------------
# Register global exception handlers
# ----------------------------
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


@app.get("/")
def root():
    return {"message": "Task Management API running"}
