from uuid import UUID
from pydantic import BaseModel, EmailStr, ConfigDict


class DoctorBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class DoctorRead(DoctorBase):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
