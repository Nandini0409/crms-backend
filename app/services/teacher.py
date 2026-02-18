from app.repositories.teacher import get_teacher_by_user_id
from app.repositories.teacherBatch import get_batches_for_teacher, is_teacher_assigned
from app.repositories.attendance import attendance_exists, create_attendance
from app.repositories.enrollment import get_students_by_batch_id, get_enrollment_by_student_batch
from app.core.exception import BusinessError, AuthError


def get_teacher_batches_service(db, user_id, batch_id: str = None):
    teacher = get_teacher_by_user_id(db, user_id)

    if not teacher:
        raise BusinessError(
            code="TEACHER_NOT_FOUND",
            user_message="Teacher profile not found",
        )

    batches = get_batches_for_teacher(db, teacher.teacher_id)

    response = []

    for batch in batches:
        batch_data = {
            "batch_id": batch.batch_id,
            "name": batch.name,
            "course": batch.course,
            "schedule": batch.schedule,
            "created_at": batch.created_at,
        }

        if batch_id is not None:
            if str(batch.batch_id) == str(batch_id):
                return batch_data
        else:
            response.append(batch_data)

    if batch_id is not None:
        raise BusinessError(
            code="BATCH_NOT_FOUND",
            user_message="Batch not found",
        )

    return response








def get_students_of_batch_service(
    db,
    *,
    user_id,
    batch_id
):
    
    teacher = get_teacher_by_user_id(db, user_id)
    if not teacher:
        raise AuthError(
            code="TEACHER_NOT_FOUND",
            user_message="Teacher profile not found"
        )
    print(teacher.teacher_id)

    teacher_batch = is_teacher_assigned(db, teacher.teacher_id, batch_id)
    if not teacher_batch:
        raise BusinessError(
            code="FORBIDDEN",
            user_message="You are not assigned to this batch"
        )

    students = get_students_by_batch_id(db, batch_id)

    return students












def mark_attendance_service(db, user, data):
    teacher = get_teacher_by_user_id(db, user.user_id)
    if not teacher:
        raise AuthError(
            code="TEACHER_NOT_FOUND",
            user_message="Teacher profile not found"
        )
    if not is_teacher_assigned(db, teacher.teacher_id, data.batch_id):
        raise BusinessError(
            code="UNAUTHORIZED_BATCH",
            user_message="You are not assigned to this batch"
        )

    created_attendance = []

    for record in data.records:

        enrollment = get_enrollment_by_student_batch(
            db,
            student_id=record.student_id,
            batch_id=data.batch_id
        )

        if not enrollment:
            raise BusinessError(
                code="STUDENT_NOT_ENROLLED",
                user_message="Student is not enrolled in this batch"
            )

        if attendance_exists(db, enrollment.enrollment_id, data.date):
            raise BusinessError(
                code="ATTENDANCE_ALREADY_MARKED",
                user_message="Attendance already marked for this date"
            )

        attendance = create_attendance(
            db,
            enrollment_id=enrollment.enrollment_id,
            date=data.date,
            status=record.status
        )

        created_attendance.append(attendance)

    return created_attendance
