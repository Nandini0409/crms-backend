from app.models.Fee import Fee
from app.models.Enrollment import Enrollment
from app.models.Payment import Payment
from app.models.Batch import Batch
from sqlmodel import select
from sqlalchemy import func

def get_fee_by_batch(db, batch_id):
    return db.query(Fee).filter(Fee.batch_id == batch_id).first()

def create_fee(db, batch_id, amount, period=None):
    fee = Fee(
        batch_id=batch_id,
        amount=amount,
        period=period
    )
    db.add(fee)
    db.flush()
    db.refresh(fee)
    return fee

def get_all_fees(db):
    return db.query(Fee).all()



def get_fees_by_batch_id(db, batch_id):
    return db.query(Fee).filter(Fee.batch_id == batch_id).all()




def get_total_fee_of_student(db, student_id):
    stmt = (
        select(func.coalesce(func.sum(Fee.amount), 0))
        .join(Batch, Batch.batch_id == Fee.batch_id)
        .join(Enrollment, Enrollment.batch_id == Batch.batch_id)
        .where(Enrollment.student_id == student_id)
    )
    return db.exec(stmt).one()




def get_total_paid_fee_of_student(db, student_id):
    stmt = (
        select(func.coalesce(func.sum(Payment.amount), 0))
        .where(Payment.student_id == student_id)
    )
    return db.exec(stmt).one()