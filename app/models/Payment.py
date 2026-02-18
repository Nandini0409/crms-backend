from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, timezone

class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    payment_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    student_id: UUID = Field(
        foreign_key="students.student_id",
        nullable=False
    )

    fee_id: UUID = Field(
        foreign_key="fees.fee_id",
        nullable=False
    )

    amount_paid: int = Field(nullable=False)

    payment_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )


    mode: str = Field(nullable=False)  
