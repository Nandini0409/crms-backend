from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.v1.auth.routes import router as auth_router
from app.api.v1.admin.routes import router as admin_router
from app.api.v1.teacher.routes import router as teacher_router
from app.api.v1.student.routes import router as student_router
from app.core.handler import register_exception_handlers

setup_logging()

origins = [origin.strip() for origin in (settings.cors_origins or "").split(",") if origin.strip()]

app = FastAPI(title=settings.app_name)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(teacher_router, prefix="/api/v1")
app.include_router(student_router, prefix="/api/v1")

register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


