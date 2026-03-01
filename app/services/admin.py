import logging

from app.repositories.user import get_user_by_email, create_user
from app.repositories.student import create_student, get_all_students, get_student_by_id, count_total_students
from app.repositories.teacher import create_teacher, get_all_teachers, get_teacher_by_id, count_total_teachers
from app.repositories.batch import create_batch, get_all_batches, get_batch_by_id, count_total_batches
from app.repositories.enrollment import get_enrollment_by_student_batch, create_enrollment, get_students_by_batch_id, get_active_enrollment
from app.repositories.teacherBatch import get_assignment_by_teacher_batch, assign_teacher, get_teachers_by_batch_id
from app.repositories.fee import get_fee_by_batch, get_all_fees, create_fee
from app.repositories.payment import get_all_payments, create_payment, sum_total_payments
from app.utils.password import hash_password, generate_random_password
from app.core.exception import BusinessError
from app.utils.email import send_welcome_email

logger = logging.getLogger(__name__)


def get_dashboard_data_service(db):
    total_students = count_total_students(db)
    total_teachers = count_total_teachers(db)
    active_batches = count_total_batches(db)
    total_payments = sum_total_payments(db)

    return {
        "totalStudents": total_students,
        "totalTeachers": total_teachers,
        "activeBatches": active_batches,
        "totalPayments": total_payments,
    }



def create_student_service(db, data):
    if get_user_by_email(db, data.email):
        raise BusinessError(
            code="USER_ALREADY_EXISTS",
            user_message="User already exists with this email",
            dev_message=f"Student creation attempted for existing email: {data.email}",
        )

    raw_password = generate_random_password()
    password_hash = hash_password(raw_password)

    user = create_user(
        db,
        email=data.email,
        password_hash=password_hash,
        role="student",
    )

    student = create_student(
        db,
        user_id=user.user_id,
        name=data.name,
        phone=data.phone,
    )

    send_welcome_email(data.email, raw_password)

    logger.info(
        "Student created successfully",
        extra={"student_id": str(student.student_id)}
    )

    return {
            "student": student,
        }



def get_all_students_service(db):
    students = get_all_students(db)
    return {
        "students": students
    }




def create_teacher_service(db, data):
    if get_user_by_email(db, data.email):
        raise BusinessError(
            code="USER_ALREADY_EXISTS",
            user_message="User already exists with this email",
            dev_message=f"Teacher creation attempted for existing email: {data.email}",
        )
    
    raw_password = generate_random_password()
    password_hash = hash_password(raw_password)

    user = create_user(
        db,
        email=data.email,
        password_hash=password_hash,
        role="teacher",
    )

    teacher = create_teacher(
        db,
        user_id=user.user_id,
        name=data.name,
        phone=data.phone,
    )

    send_welcome_email(data.email, raw_password)

    logger.info(
        "Teacher created successfully",
        extra={"teacher_id": str(teacher.teacher_id)}
    )

    return {
            "teacher": teacher,
        }


def get_all_teachers_service(db):
    teachers = get_all_teachers(db)
    return {
        "teachers": teachers
    }





def create_batch_service(db, data):
    batch = create_batch(
    db,
    name=data.name,
    course=data.course,
    schedule=data.schedule
    )

    logger.info(
        "batch created successfully",
        extra={"batch_id": str(batch.batch_id)}
    )

    return {
        "batch": batch
    }





def get_all_batch_service(db):
    batches = get_all_batches(db)
    return {
        "batches": batches
    }



def get_teachers_with_batchid_service(batch_id, db):
    print("hii")
    teachers = get_teachers_by_batch_id(batch_id, db)
    return {
        "teachers": teachers
    }




def get_students_with_batchid_service(batch_id, db):
    students = get_students_by_batch_id(batch_id, db)
    return {
        "students": students
    }





def enroll_student_service(db, data):
    student = get_student_by_id(db, data.student_id)
    if not student:
        raise BusinessError(
            code="STUDENT_NOT_FOUND",
            user_message="Student not found",
            status_code=404
        )

    
    batch = get_batch_by_id(db, data.batch_id)
    if not batch:
        raise BusinessError(
            code="BATCH_NOT_FOUND",
            user_message="Batch not found",
            status_code=404
        )

    existing_enrollment = get_enrollment_by_student_batch(
        db,
        data.student_id,
        data.batch_id
    )

    if existing_enrollment:
        raise BusinessError(
            code="ALREADY_ENROLLED",
            user_message="Student is already enrolled in this batch"
        )

    enrollment = create_enrollment(
        db,
        student_id=data.student_id,
        batch_id=data.batch_id
    )

    logger.info(
        "Student enrolled successfully",
        extra={
            "student_id": str(data.student_id),
            "batch_id": str(data.batch_id),
        }
    )

    return {
        "enrollment": enrollment
    }    



def assign_teacher_batch_service(db, data):
    teacher = get_teacher_by_id(db, data.teacher_id)
    if not teacher:
        raise BusinessError(
            code="TEACHER_NOT_FOUND",
            user_message="Teacher not found",
            status_code=404
        )

    batch = get_batch_by_id(db, data.batch_id)
    if not batch:
        raise BusinessError(
            code="BATCH_NOT_FOUND",
            user_message="Batch not found",
            status_code=404
        )

    existing_assignment = get_assignment_by_teacher_batch(
        db,
        data.teacher_id,
        data.batch_id
    )

    if existing_assignment:
        raise BusinessError(
            code="ALREADY_ASSIGNED",
            user_message="Teacher is already assigned to this batch."
        )

    assignment = assign_teacher(
        db,
        teacher_id=data.teacher_id,
        batch_id=data.batch_id
    )

    logger.info(
        "Teacher assigned successfully.",
        extra={
            "teacher_id": str(data.teacher_id),
            "batch_id": str(data.batch_id),
        }
    )

    return {
        "assignment": assignment
    }





def create_fee_service(db, data):
    batch = get_batch_by_id(db, data.batch_id)
    if not batch:
        raise BusinessError(
            code="BATCH_NOT_FOUND",
            user_message="Batch not found",
            status_code=404
        )

    existing_fee = get_fee_by_batch(db, data.batch_id)
    if existing_fee:
        raise BusinessError(
            code="FEE_ALREADY_EXISTS",
            user_message="Fee already defined for this batch"
        )

    fee = create_fee(
        db,
        batch_id=data.batch_id,
        amount=data.amount,
        period=data.period
    )

    return {
        "fee": fee
        }




def get_batch_fee_service(db):
    fees = get_all_fees(db)
    return {
        "fees": fees
        }




def create_payment_service(db, data):
    student = get_student_by_id(db, data.student_id)
    if not student:
        raise BusinessError(
            code="STUDENT_NOT_FOUND",
            user_message="Student not found",
            status_code=404
        )

    batch = get_batch_by_id(db, data.batch_id)
    if not batch:
        raise BusinessError(
            code="BATCH_NOT_FOUND",
            user_message="Batch not found",
            status_code=404
        )
    

    enrollment = get_active_enrollment(db, data.student_id, data.batch_id)
    if not enrollment:
        raise BusinessError(
            code="STUDENT_NOT_ENROLLED",
            user_message="Student is not enrolled in this batch",
            status_code=400
        )


    fee = get_fee_by_batch(db, data.batch_id)
    if not fee:
        raise BusinessError(
            code="FEE_NOT_DEFINED",
            user_message="Fee not defined for this batch"
        )

    if data.amount_paid <= 0:
        raise BusinessError(
            code="INVALID_PAYMENT_AMOUNT",
            user_message="Payment amount must be greater than zero"
        )

    if data.amount_paid > fee.amount:
        raise BusinessError(
            code="INVALID_PAYMENT",
            user_message="Payment amount exceeds batch fee"
        )

    payment = create_payment(
        db=db,
        student_id=data.student_id,
        fee_id=fee.fee_id,
        amount_paid=data.amount_paid,
        mode=data.mode
    )

    return {
        "payment": payment
    }




def get_all_payment_service(db):
    payments = get_all_payments(db)
    return {"payments": payments}