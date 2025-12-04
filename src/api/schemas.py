# src/api/schemas.py
from pydantic import BaseModel, EmailStr


# ---------- Utilisateurs ----------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True  # Pydantic v2


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ---------- Analyses ----------

class PatientInfo(BaseModel):
    name: str | None = None
    age: str | None = None
    sex: str | None = None


class AnalysisOut(BaseModel):
    id: int
    prediction: str
    model: str
    report_pdf: str
    patient: PatientInfo

    class Config:
        from_attributes = True
