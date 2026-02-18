from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.core.deps import get_current_user, student_require
from app.services.student import (
  get_student_attendance_service,
  get_student_fees_service,
  get_student_batch_service,
  get_dashboard_data_service
)
from app.schemas.base import APIResponse
from fastapi import Query
from uuid import UUID

router = APIRouter(prefix="/student", tags=["Student"])



@router.get("/dashboard", response_model=APIResponse)
def get_dashboard_data_route(
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user),
    _=Depends(student_require)
):
    result = get_dashboard_data_service(db, current_user)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }





@router.get("/attendance", response_model=APIResponse)
def get_student_attendance_route(
    batch_id: UUID | None = Query(default=None),
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user),
    _ = Depends(student_require)
):
    data = get_student_attendance_service(
        db=db,
        user_id=current_user.user_id,
        batch_id=batch_id
    )

    return {
        "success": True,
        "message": "Attendance fetched successfully",
        "detail": data
    }


@router.get("/fees", response_model=APIResponse)
def get_my_fees_route(
    batch_id: UUID | None = Query(default=None),
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user),
    _ = Depends(student_require)
):
    data = get_student_fees_service(
        db=db,
        user_id=current_user.user_id,
        batch_id=batch_id    
    )

    return {
        "success": True,
        "message": "Fees fetched successfully",
        "detail": data
    }



@router.get("/batch", response_model=APIResponse)
def get_my_batch_route(
    batch_id: UUID | None = Query(default=None),
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user),
    _ = Depends(student_require)
):
    data = get_student_batch_service(
        db=db,
        user_id=current_user.user_id,
        batch_id=batch_id
    )
    return {
        "success": True,
        "message": "Batch fetched successfully",
        "detail": data
    }

