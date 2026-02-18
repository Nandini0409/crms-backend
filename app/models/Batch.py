from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class Batch(SQLModel, table=True):
    __tablename__ = "batches"

    batch_id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )

    name: str = Field(nullable=False)
    course: str = Field(nullable=False)

    schedule: str = Field(
        nullable=False,
        description="Human readable schedule like 'Mon-Wed-Fri 6-7 PM'"
    )

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
