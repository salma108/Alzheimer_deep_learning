# src/utils/report.py

from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def generate_pdf_report(
    out_path: str,
    *,
    analysis_id: str,
    patient: dict,
    model_name: str,
    prediction: str,
    probabilities: dict,
    notes: str | None = None,
):
    """
    Crée un petit rapport médical PDF pour l'analyse.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(out_path), pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Rapport d'analyse IRM - Alzheimer")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"ID analyse : {analysis_id}")
    y -= 15
    c.drawString(50, y, f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    y -= 25

    # Patient
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Informations patient")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"Nom : {patient.get('name','-')}")
    y -= 15
    c.drawString(60, y, f"Âge : {patient.get('age','-')}")
    y -= 15
    c.drawString(60, y, f"Sexe : {patient.get('sex','-')}")
    y -= 25

    # Résultat
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Résultat de l'IA")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(60, y, f"Modèle utilisé : {model_name}")
    y -= 15
    c.drawString(60, y, f"Classe prédite : {prediction}")
    y -= 20

    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Probabilités par classe")
    y -= 18
    c.setFont("Helvetica", 10)
    for cls, p in probabilities.items():
        c.drawString(60, y, f"{cls} : {p*100:.2f} %")
        y -= 15

    y -= 15
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Notes / commentaires")
    y -= 18
    c.setFont("Helvetica", 10)
    txt = notes or "Aucun commentaire ajouté pour le moment."
    for line in txt.split("\n"):
        c.drawString(60, y, line)
        y -= 15

    c.showPage()
    c.save()
