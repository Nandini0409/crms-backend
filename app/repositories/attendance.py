from app.models.Attendance import Attendance
from app.models.Enrollment import Enrollment
from sqlmodel import select
from sqlalchemy import func, case
from uuid import UUID
from typing import Optional



def attendance_exists(db, enrollment_id, date):
    return (
        db.query(Attendance)
        .filter(
            Attendance.enrollment_id == enrollment_id,
            Attendance.date == date
        )
        .first()
    )


def create_attendance(db, enrollment_id, date, status):
    attendance = Attendance(
        enrollment_id=enrollment_id,
        date=date,
        status=status
    )
    db.add(attendance)
    db.flush()
    db.refresh(attendance)
    return attendance





def get_attendance_by_student_id(db, student_id: UUID, batch_id: Optional[UUID] = None):
    query = (
        db.query(
            func.count(Attendance.attendance_id).label("total_classes"),
            func.sum(
                case((Attendance.status == "PRESENT", 1), else_=0)
            ).label("present_count")
        )
        .join(Enrollment, Enrollment.enrollment_id == Attendance.enrollment_id)
        .filter(Enrollment.student_id == student_id)
    )

    if batch_id is not None:
        query = query.filter(Enrollment.batch_id == batch_id)

    return query.first()




def get_attendance_percentage(db, student_id):
    stmt_total = (
        select(func.count(Attendance.attendance_id))
        .join(Enrollment, Enrollment.enrollment_id == Attendance.enrollment_id)
        .where(Enrollment.student_id == student_id)
    )
    total_classes = db.exec(stmt_total).one()

    if total_classes == 0:
        return 0

    stmt_present = (
        select(func.count(Attendance.attendance_id))
        .join(Enrollment, Enrollment.enrollment_id == Attendance.enrollment_id)
        .where(Enrollment.student_id == student_id)
        .where(Attendance.status == "present")
    )
    present_classes = db.exec(stmt_present).one()

    return round((present_classes / total_classes) * 100)
