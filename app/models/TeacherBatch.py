from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from sqlalchemy import UniqueConstraint

class TeacherBatch(SQLModel, table=True):
    __tablename__ = "teacher_batches"
    __table_args__ = (
        UniqueConstraint("teacher_id", "batch_id"),
    )

    assignment_id: UUID = Field(default_factory=uuid4, primary_key=True)
    teacher_id: UUID = Field(foreign_key="teachers.teacher_id", nullable=False)
    batch_id: UUID = Field(foreign_key="batches.batch_id", nullable=False)
