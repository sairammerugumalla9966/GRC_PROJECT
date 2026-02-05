from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handles HTTP errors like 401, 403, 404
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail if hasattr(exc, "detail") else str(exc)
        },
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handles validation errors (body, query, path)
    """
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": exc.errors(),
            "body": exc.body
        },
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Handles DB errors
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Database error occurred",
            "details": str(exc)
        },
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """
    Handles unexpected errors
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "details": str(exc)
        },
    )
