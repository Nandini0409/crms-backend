from sqlmodel import Session, select
from app.models.Enrollment import Enrollment
from app.models.Student import Student
from app.models.Batch import Batch
from uuid import UUID


def get_enrollment_by_student_batch(
    db: Session,
    student_id: UUID,
    batch_id: UUID
) -> Enrollment | None:
    stmt = select(Enrollment).where(
        Enrollment.student_id == student_id,
        Enrollment.batch_id == batch_id
    )
    return db.exec(stmt).first()


def create_enrollment(
    db: Session,
    *,
    student_id: UUID,
    batch_id: UUID
) -> Enrollment:
    enrollment = Enrollment(
        student_id=student_id,
        batch_id=batch_id
    )
    db.add(enrollment)
    db.flush()
    db.refresh(enrollment)
    return enrollment


def get_students_by_batch_id(
    db: Session,
    batch_id
) -> list[Student]:
    return (
        db.query(Student)
        .join(Enrollment, Enrollment.student_id == Student.student_id)
        .filter(Enrollment.batch_id == batch_id)
        .all()
    )



def get_active_enrollments_by_student(db, student_id):
    return (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == student_id,
            Enrollment.status == "active"
        )
        .all()
    )





def get_batches_by_student_id(db, student_id):
    statement = (
        select(Batch)
        .join(Enrollment, Enrollment.batch_id == Batch.batch_id)
        .where(
            Enrollment.student_id == student_id,
        )
    )

    return db.exec(statement).all()





