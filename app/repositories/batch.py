from app.models.Batch import Batch
from sqlmodel import Session, select
from sqlalchemy import func


def count_total_batches(db: Session) -> int:
    statement = select(func.count()).select_from(Batch)
    result = db.exec(statement)
    return result.one()

def create_batch(
    db,
    *,
    name: str,
    course: str,
    schedule: str
) -> Batch:
    batch = Batch(
        name=name,
        course=course,
        schedule=schedule
    )
    db.add(batch)
    db.flush()
    db.refresh(batch)
    return batch


def get_all_batches(db: Session) -> list[Batch]:
    statement = select(Batch)
    results = db.exec(statement)
    return results.all()


def get_batch_by_id(db, batch_id: int) -> Batch | None:
    return db.query(Batch).filter(Batch.batch_id == batch_id).first()