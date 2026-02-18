from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.core.exception import AppError

def register_exception_handlers(app):
    @app.exception_handler(AppError)
    async def app_error_handler(_, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.user_message,
                "detail":{
                    "code": exc.code,
                    "dev_message": exc.dev_message,
                }
            },
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(_, exc):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "message": "Invalid data provided.",
                "detail":{
                    "code": "DB_CONSTRAINT_ERROR",
                    "dev_message": str(exc),
                }
            },
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(_, exc):
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Something went wrong on our end.",
                "detail":{
                    "code": "DB_ERROR",
                    "dev_message": str(exc),
                }
            },
        )
