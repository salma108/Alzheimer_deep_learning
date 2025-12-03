# src/api/analysis.py
import base64
import io
import json
import uuid
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import torch
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
from sqlalchemy.orm import Session
from torchvision import transforms
from transformers import ViTForImageClassification

from src.utils.config import get_device
from src.utils.report import generate_pdf_report
from src.xai.gradcam import generate_gradcam
from src.xai.attention_rollout import attention_rollout
from src.models.architectures import build_resnet50, build_densenet121

from .database import get_db
from .models import Analysis
from .security import get_current_user
from .schemas import PatientInfo

router = APIRouter(tags=["analysis"])

DEVICE = get_device()
BEST_INFO_PATH = Path("models/best_model.json")

# ---------- Chargement du meilleur modèle ----------


def load_best_model():
    if not BEST_INFO_PATH.exists():
        raise RuntimeError("models/best_model.json introuvable")

    with BEST_INFO_PATH.open("r", encoding="utf-8") as f:
        info = json.load(f)

    best = info["best"]
    class_names = info["class_names"]
    name = best["name"]
    path = best["path"]

    if name == "ResNet50":
        model = build_resnet50(len(class_names))
        state = torch.load(path, map_location=DEVICE)
        model.load_state_dict(state)
    elif name == "DenseNet121":
        model = build_densenet121(len(class_names))
        state = torch.load(path, map_location=DEVICE)
        model.load_state_dict(state)
    elif name == "ViT":
        model = ViTForImageClassification.from_pretrained(path)
    else:
        raise ValueError(f"Modèle inconnu dans best_model.json : {name}")

    model.to(DEVICE).eval()
    return model, name, class_names


MODEL, MODEL_NAME, CLASS_NAMES = load_best_model()

PRED_TRANSFORM = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.5] * 3, [0.5] * 3),
    ]
)


# ---------- /predict (protégé) ----------


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    patient_name: str = Form("Inconnu"),
    patient_age: str = Form(""),
    patient_sex: str = Form(""),
    notes: str = Form(""),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # 1) Lecture image
    content = await file.read()
    try:
        img = Image.open(io.BytesIO(content)).convert("RGB")
    except Exception:
        raise HTTPException(status_code=400, detail="Image invalide")

    # 2) Préparation modèle
    tensor = PRED_TRANSFORM(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = MODEL(tensor)
        logits = outputs.logits if hasattr(outputs, "logits") else outputs
        probs = torch.softmax(logits, dim=1)[0].cpu().numpy()

    pred_idx = int(probs.argmax())
    prediction = CLASS_NAMES[pred_idx]
    prob_dict = {cls: float(probs[i]) for i, cls in enumerate(CLASS_NAMES)}

    # 3) XAI
    img_for_xai = PRED_TRANSFORM(img).to(DEVICE)

    if MODEL_NAME in ["ResNet50", "DenseNet121"]:
        if MODEL_NAME == "ResNet50":
            target_layer = MODEL.layer4[-1].conv3
        else:
            target_layer = MODEL.features[-1]
        heat = generate_gradcam(MODEL, img_for_xai, target_layer)
    else:
        heat = attention_rollout(MODEL, img_for_xai)

    heat = (heat - heat.min()) / (heat.max() - heat.min() + 1e-8)
    heat_uint8 = np.uint8(heat * 255)
    heat_color = cv2.applyColorMap(heat_uint8, cv2.COLORMAP_JET)
    heat_color = cv2.cvtColor(heat_color, cv2.COLOR_BGR2RGB)

    orig = np.array(img.resize((heat_color.shape[1], heat_color.shape[0])))
    overlay = cv2.addWeighted(orig, 0.6, heat_color, 0.4, 0)

    metrics_dir = Path("metrics")
    metrics_dir.mkdir(exist_ok=True)
    analysis_uid = str(uuid.uuid4())[:8]
    xai_path = metrics_dir / f"xai_{analysis_uid}.png"
    cv2.imwrite(str(xai_path), cv2.cvtColor(overlay, cv2.COLOR_RGB2BGR))

    with xai_path.open("rb") as f:
        xai_b64 = base64.b64encode(f.read()).decode("utf-8")

    # 4) PDF
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    pdf_path = reports_dir / f"report_{analysis_uid}.pdf"

    patient = {"name": patient_name, "age": patient_age, "sex": patient_sex}
    generate_pdf_report(
        out_path=str(pdf_path),
        analysis_id=analysis_uid,
        patient=patient,
        model_name=MODEL_NAME,
        prediction=prediction,
        probabilities=prob_dict,
        notes=notes,
    )

    report_url = f"http://localhost:8000/static/reports/report_{analysis_uid}.pdf"

    # 5) Sauvegarde DB
    db_analysis = Analysis(
        patient_name=patient_name,
        patient_age=patient_age,
        patient_sex=patient_sex,
        prediction=prediction,
        model_name=MODEL_NAME,
        report_pdf=report_url,
        notes=notes,
        owner_id=current_user.id,
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)

    # 6) Réponse JSON
    return JSONResponse(
        {
            "id": db_analysis.id,
            "model": MODEL_NAME,
            "prediction": prediction,
            "probabilities": prob_dict,
            "xai": xai_b64,
            "report_pdf": report_url,
            "patient": patient,
        }
    )
