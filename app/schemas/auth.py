from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
  email: EmailStr
  password: str



class ChangePasswordRequest(BaseModel):
  email: EmailStr
  current_password: str = Field(..., min_length=8)
  new_password: str = Field(..., min_length=8)

