# src/api/history.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Analysis
from .security import get_current_user

router = APIRouter(tags=["history"])


@router.get("/history")
def get_history(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    analyses = (
        db.query(Analysis)
        .filter(Analysis.owner_id == current_user.id)
        .order_by(Analysis.created_at.desc())
        .all()
    )

    items = []
    for a in analyses:
        items.append(
            {
                "id": a.id,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "patient": {
                    "name": a.patient_name,
                    "age": a.patient_age,
                    "sex": a.patient_sex,
                },
                "prediction": a.prediction,
                "model": a.model_name,
                "report": a.report_pdf,
            }
        )
    return items
