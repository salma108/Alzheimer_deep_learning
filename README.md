# Alzheimer Project – Classification IRM 

Ce projet implémente une pipeline complète pour la classification d'IRM cérébrales
(4 classes Alzheimer) avec :

- 3 modèles : **ResNet50**, **DenseNet121**, **ViT**
- Augmentations : classiques + **RandAugment** + **MixUp / CutMix**
- **Early stopping** pour tous les modèles
- Comparaison équitable (mêmes données, mêmes hyperparamètres)
- **XAI** : Grad-CAM (CNN) et attention rollout (ViT)
- MLOps : **DVC** (+ remote S3 à configurer), logs basiques
- API **FastAPI**
- Frontend **React (Vite)** pour l'application médecin
- Dockerisation (backend + frontend)

## Commandes principales

### 1. Installation (Python)

```bash
python -m venv .venv
source .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Préparation des données

Placer le dataset dans :

```text
data/raw/Alzheimer_MRI_4_classes_dataset/
  MildDemented/
  ModerateDemented/
  NonDemented/
  VeryMildDemented/
```

Puis :

```bash
python -m src.data.prepare_data
```

### 3. Entraînement des 3 modèles (5 epochs chacun)

```bash
python -m src.models.train_all
```

Les meilleurs poids seront enregistrés dans `models/` et un fichier
`models/best_model.json` indiquera le meilleur modèle.

### 4. Lancer l'API

```bash
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Lancer le frontend React

```bash
cd frontend
npm install
npm run dev
```

Puis ouvrir l'URL affichée (par défaut http://localhost:5173).

### 6. Docker (optionnel)

```bash
cd docker
docker compose up --build
```

---

---

##  Visualisations automatiques

Pour générer toutes les visualisations (échantillons, distribution de classes, augmentations, MixUp/CutMix, PCA, t-SNE) :

```bash
python -m src.models.visualizations
```

Les images seront enregistrées dans le dossier `metrics/`.

##  Rapport d'évaluation

Après l'entraînement, génère un rapport global (JSON + HTML) :

```bash
python -m src.models.evaluation
```

- Résumé : `metrics/final_summary.json`
- Rapport HTML : `metrics/report.html` (exportable en PDF depuis le navigateur)

## Dashboard Streamlit

Pour un tableau de bord interactif (résultats + visualisations + XAI) :

```bash
streamlit run src/models/dashboard_streamlit.py
```

Assure-toi que :

- les modèles sont entraînés (`python -m src.models.train_all`)
- les visualisations sont générées (`python -m src.models.visualizations`)
