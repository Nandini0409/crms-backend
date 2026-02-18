from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_session
from app.core.deps import get_current_user, teacher_require
from app.services.teacher import (
  get_teacher_batches_service,
  mark_attendance_service,
  get_students_of_batch_service
)
from app.schemas.base import APIResponse
from app.schemas.request import MarkAttendanceRequest
from fastapi import Query
from uuid import UUID


router = APIRouter(prefix="/teacher", tags=["Teacher"])


@router.get("/batches", response_model=APIResponse)
def get_teacher_batches_route(
    batch_id: UUID | None = Query(default=None),
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user),
    _ = Depends(teacher_require)
):
    result = get_teacher_batches_service(
        db=db,
        user_id=current_user.user_id,
        batch_id=batch_id
    )
    return {
        "success": True,
        "message": "successfull response",
        "detail": result
    }


@router.post(
    "/attendance",
    response_model=APIResponse
)
def mark_attendance_route(
    data: MarkAttendanceRequest,
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user),
    _ = Depends(teacher_require)
):
    mark_attendance_service(db, current_user, data)

    return {
        "success": True,
        "message": "Attendance marked successfully",
        "detail": None
    }




@router.get(
    "/batches/{batch_id}/students",
    response_model=APIResponse
)
def get_students_of_batch_route(
    batch_id: str,
    db: Session = Depends(get_session),
    current_user = Depends(get_current_user),
    _ = Depends(teacher_require)
):
    students = get_students_of_batch_service(
        db,
        user_id=current_user.user_id,
        batch_id=batch_id
    )

    return {
        "success": True,
        "message": "Successfull response.",
        "detail": students
    }
