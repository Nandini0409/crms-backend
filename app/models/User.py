from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Boolean, String, DateTime
from sqlalchemy.dialects.postgresql import UUID as PG_UUID


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: UUID = Field(
        default_factory=uuid4,
        sa_column=Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            nullable=False
        )
    )

    email: str = Field(
        sa_column=Column(
            String(255),
            nullable=False,
            unique=True,
            index=True
        )
    )

    password_hash: str = Field(
        sa_column=Column(
            String(255),
            nullable=False
        )
    )

    role: str = Field(
        default="user",
        sa_column=Column(
            String(50),
            nullable=False
        )
    )

    is_first_login: bool = Field(
        default=True,
        sa_column=Column(Boolean, nullable=False)
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False)
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), nullable=False, onupdate=lambda: datetime.now(timezone.utc))
    )
