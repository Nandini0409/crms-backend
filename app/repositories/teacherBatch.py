from sqlmodel import Session, select
from app.models.TeacherBatch import TeacherBatch
from app.models.Teacher import Teacher
from uuid import UUID
from app.models.Batch import Batch


def get_assignment_by_teacher_batch(
    db: Session,
    teacher_id: UUID,
    batch_id: UUID
) -> TeacherBatch | None:
    stmt = select(TeacherBatch).where(
        TeacherBatch.teacher_id == teacher_id,
        TeacherBatch.batch_id == batch_id
    )
    return db.exec(stmt).first()


def assign_teacher(
    db: Session,
    *,
    teacher_id: UUID,
    batch_id: UUID
) -> TeacherBatch:
    assignment = TeacherBatch(
        teacher_id=teacher_id,
        batch_id=batch_id
    )
    db.add(assignment)
    db.flush()
    db.refresh(assignment)
    return assignment



def get_batches_for_teacher(db, teacher_id):
    return (
        db.query(Batch)
        .join(TeacherBatch, TeacherBatch.batch_id == Batch.batch_id)
        .filter(TeacherBatch.teacher_id == teacher_id)
        .all()
    )



def is_teacher_assigned(db, teacher_id: UUID, batch_id: UUID) -> bool:
    return db.query(TeacherBatch).filter(
        TeacherBatch.teacher_id == teacher_id,
        TeacherBatch.batch_id == batch_id
    ).first() is not None





def get_teachers_by_batch_id(
    db: Session,
    batch_id
) -> list[Teacher]:
    return (
        db.query(Teacher)
        .join(TeacherBatch, TeacherBatch.teacher_id == Teacher.teacher_id)
        .filter(TeacherBatch.batch_id == batch_id)
        .all()
    )