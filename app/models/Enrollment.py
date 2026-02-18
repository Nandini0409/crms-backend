from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


from sqlalchemy import UniqueConstraint

class Enrollment(SQLModel, table=True):
    __tablename__ = "enrollments"
    __table_args__ = (
        UniqueConstraint("student_id", "batch_id", name="uq_student_batch"),
    )

    enrollment_id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )

    student_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("students.student_id"),
            nullable=False
        )
    )

    batch_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("batches.batch_id"),
            nullable=False
        )
    )

    enroll_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    status: str = Field(default="active", nullable=False)
