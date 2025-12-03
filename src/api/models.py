# src/api/models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    analyses = relationship(
        "Analysis", back_populates="owner", cascade="all, delete-orphan"
    )


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    patient_name = Column(String, nullable=True)
    patient_age = Column(String, nullable=True)
    patient_sex = Column(String, nullable=True)

    prediction = Column(String, nullable=False)
    model_name = Column(String, nullable=False)
    report_pdf = Column(String, nullable=False)
    notes = Column(String, nullable=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="analyses")
