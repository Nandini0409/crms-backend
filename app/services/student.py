from app.repositories.student import get_student_by_user_id
from app.repositories.attendance import get_attendance_by_student_id, get_attendance_percentage
from app.repositories.enrollment import get_active_enrollment, get_batches_by_student_id
from app.repositories.fee import get_fees_by_batch_id
from app.repositories.payment import get_total_paid_by_student_and_fee_ids
from app.core.exception import AuthError
from uuid import UUID





def get_dashboard_data_service(db, user):
    student = get_student_by_user_id(db, user.user_id)
    if not student:
        raise AuthError(
            code="STUDENT_NOT_FOUND",
            user_message="Student profile not found"
        )
    


    enrollments = get_active_enrollments_by_student(db, student.student_id)

    total_batches = len(enrollments)
    total_fee = 0
    total_paid = 0

    for enrollment in enrollments:
        fees = get_fees_by_batch_id(db, enrollment.batch_id)

        if not fees:
            continue

        batch_total_fee = sum(fee.amount for fee in fees)
        fee_ids = [fee.fee_id for fee in fees]

        batch_paid = get_total_paid_by_student_and_fee_ids(
            db,
            student.student_id,
            fee_ids
        )

        total_fee += batch_total_fee
        total_paid += batch_paid

    attendance_percent = get_attendance_percentage(db, student.student_id)

    return {
        "totalBatches": total_batches,
        "fees": {
            "paid": total_paid,
            "total": total_fee
        },
        "attendancePercent": attendance_percent
    }





def get_student_attendance_service(db, user_id, batch_id: UUID | None = None):
    student = get_student_by_user_id(db, user_id)

    if not student:
        raise AuthError(
            code="STUDENT_NOT_FOUND",
            user_message="Student profile not found"
        )

    result = get_attendance_by_student_id(
        db=db,
        student_id=student.student_id,
        batch_id=batch_id
    )

    total_classes = result.total_classes or 0
    present = result.present_count or 0
    absent = total_classes - present
    percentage = round((present / total_classes) * 100, 2) if total_classes else 0

    return {
        "total_classes": total_classes,
        "present": present,
        "absent": absent,
        "percentage": percentage
    }




def get_student_fees_service(db, user_id, batch_id: int | None = None):
    student = get_student_by_user_id(db, user_id)
    if not student:
        raise AuthError(
            code="STUDENT_NOT_FOUND",
            user_message="Student profile not found"
        )

    enrollments = get_active_enrollment(db, student.student_id)

    response = []

    for enrollment in enrollments:
        if batch_id and enrollment.batch_id != batch_id:
            continue

        fees = get_fees_by_batch_id(db, enrollment.batch_id)

        total_fee = sum(fee.amount for fee in fees)
        fee_ids = [fee.fee_id for fee in fees]

        total_paid = get_total_paid_by_student_and_fee_ids(
            db,
            student.student_id,
            fee_ids
        )

        remaining = total_fee - total_paid

        percentage = (
            round((total_paid / total_fee) * 100, 2)
            if total_fee > 0 else 0
        )

        response.append({
            "batch_id": enrollment.batch_id,
            "total_fee": total_fee,
            "paid": total_paid,
            "remaining": remaining,
            "percentage": percentage
        })

    return response






def get_student_batch_service(db, user_id, batch_id: int = None):
    student = get_student_by_user_id(db, user_id)
    print(batch_id)

    if not student:
        raise AuthError(
            code="STUDENT_NOT_FOUND",
            user_message="Student profile not found"
        )

    batches = get_batches_by_student_id(db, student.student_id)

    response = []

    for batch in batches:
        batch_data = {
            "batch_id": batch.batch_id,
            "name": batch.name,
            "course": batch.course,
            "schedule": batch.schedule,
            "created_at": batch.created_at
        }

        if batch_id is not None:
            if batch.batch_id == batch_id:
                return batch_data  
        else:
            response.append(batch_data)

    if batch_id is not None:
        raise AuthError(
            code="BATCH_NOT_FOUND",
            user_message="Batch not found"
        )

    return response





