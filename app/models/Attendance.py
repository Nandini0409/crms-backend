from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import UniqueConstraint, ForeignKey
from datetime import date as DateType

class Attendance(SQLModel, table=True):
    __tablename__ = "attendance"
    __table_args__ = (
        UniqueConstraint("enrollment_id", "date", name="uq_attendance_day"),
    )

    attendance_id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )

    enrollment_id: UUID = Field(
        sa_column=Column(
            PG_UUID(as_uuid=True),
            ForeignKey("enrollments.enrollment_id"),
            nullable=False
        )
    )

    date: DateType = Field(nullable=False)

    status: str = Field(nullable=False) 
