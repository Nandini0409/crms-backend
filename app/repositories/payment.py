from app.models.Payment import Payment
from datetime import datetime, timezone
from sqlalchemy import func
from sqlmodel import Session, select
from app.models.Student import Student
from app.models.Fee import Fee
from app.models.Batch import Batch



def get_all_payments(db):
    statement = (
        select(Payment, Student, Batch)
        .join(Student, Payment.student_id == Student.student_id)
        .join(Fee, Payment.fee_id == Fee.fee_id)
        .join(Batch, Fee.batch_id == Batch.batch_id)
    )

    results = db.exec(statement).all()

    payments = []

    for payment, student, batch in results:
        payments.append({
            "payment_id": payment.payment_id,
            "student_name": student.name,
            "batch_name": batch.name,
            "amount_paid": payment.amount_paid,
            "payment_date": payment.payment_date,
            "mode": payment.mode
        })

    return payments


def sum_total_payments(db: Session) -> float:
    statement = select(func.sum(Payment.amount_paid))
    result = db.exec(statement).one()
    return result if result is not None else 0






def create_payment(db, student_id, fee_id, amount_paid, mode):
    payment = Payment(
        student_id=student_id,
        fee_id=fee_id,
        amount_paid=amount_paid,
        payment_date=datetime.now(timezone.utc),
        mode=mode
    )
    db.add(payment)
    db.flush()
    db.refresh(payment)
    return payment





def get_total_paid_by_student_and_fee_ids(db, student_id, fee_ids):
    if not fee_ids:
        return 0

    total = (
        db.query(func.coalesce(func.sum(Payment.amount_paid), 0))
        .filter(
            Payment.student_id == student_id,
            Payment.fee_id.in_(fee_ids)
        )
        .scalar()
    )

    return total
