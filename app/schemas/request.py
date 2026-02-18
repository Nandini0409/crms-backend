from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
from datetime import date, datetime
from typing import Optional, Literal, List
import re
from enum import Enum

class CreateStudentRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None

    @field_validator("phone")
    def validate_phone(cls, v):
        if v is None:
            return v

        if not re.fullmatch(r"\d{10}", v):
            raise ValueError("Phone must be 10 digits")

        return v



class CreateTeacherRequest(BaseModel):
  email: EmailStr
  name: str = Field(..., min_length=1)
  phone: Optional[str] = None


class CreateEnrollmentRequest(BaseModel):
  student_id: UUID
  batch_id: UUID


class AssignTeacherBatchRequest(BaseModel):
  teacher_id: UUID
  batch_id: UUID


class CreateBatchRequest(BaseModel):
  name: str
  course: str
  schedule: str


class CreateFeeRequest(BaseModel):
  batch_id: UUID
  amount: int = Field(..., gt=0)
  period: str = Field(..., example="Jan 2026")



class PaymentMode(str, Enum):
    cash = "cash"
    upi = "upi"
    card = "card"
    bank_transfer = "bank_transfer"


class CreatePaymentRequest(BaseModel):
  student_id: UUID
  batch_id: UUID
  amount_paid: int = Field(..., gt=0)
  payment_date: datetime
  mode: PaymentMode = Field(nullable=False)




class AttendanceRecordIn(BaseModel):
  student_id: UUID
  status: Literal["PRESENT", "ABSENT"]


class MarkAttendanceRequest(BaseModel):
  batch_id: UUID
  date: date
  records: List[AttendanceRecordIn]
