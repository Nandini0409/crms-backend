from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from decimal import Decimal
class Fee(SQLModel, table=True):
    __tablename__ = "fees"

    fee_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True
    )

    batch_id: UUID = Field(
        foreign_key="batches.batch_id",
        nullable=False
    )

    amount: int = Field(nullable=False)

    period: str = Field(nullable=False)  
