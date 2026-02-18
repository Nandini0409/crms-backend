from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import (
    LoginRequest,
    ChangePasswordRequest
)
from app.core.deps import get_current_user
from app.services.auth import (
    login_service,
    force_change_password_service,
    get_my_profile_service
)
from app.schemas.base import APIResponse
from app.db.session import get_session

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.get("/me", response_model=APIResponse)
def get_my_profile_route(
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user)
):
    result = get_my_profile_service(db, current_user)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }



@router.post("/login", response_model=APIResponse)
def login_route(
    data: LoginRequest,
    db: Session = Depends(get_session)
):
    result = login_service(data, db)
    return {
        "success": True,
        "message": "Login successful.",
        "detail": result
    }


@router.post("/force-change-password", response_model=APIResponse)
def force_change_password_route(
    data: ChangePasswordRequest,
    db: Session = Depends(get_session)
):
    result = force_change_password_service(data, db)
    return {
        "success": True,
        "message": "Password changed successfully",
        "detail": result
    }

