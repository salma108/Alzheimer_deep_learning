from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
import json
import matplotlib.pyplot as plt
import seaborn as sns

def save_classification_report(y_true, y_pred, class_names, out_path: str):
  out = Path(out_path)
  out.parent.mkdir(parents=True, exist_ok=True)
  rep = classification_report(y_true, y_pred, target_names=class_names, output_dict=True)
  with out.open("w", encoding="utf-8") as f:
    json.dump(rep, f, indent=2)

def save_confusion_matrix(y_true, y_pred, class_names, out_path: str, title: str = ""):
  cm = confusion_matrix(y_true, y_pred)
  fig, ax = plt.subplots(figsize=(6,5))
  sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
              xticklabels=class_names, yticklabels=class_names, ax=ax)
  ax.set_xlabel("Prédiction")
  ax.set_ylabel("Vérité")
  if title:
    ax.set_title(title)
  out = Path(out_path)
  out.parent.mkdir(parents=True, exist_ok=True)
  fig.tight_layout()
  fig.savefig(out, dpi=150)
  plt.close(fig)
