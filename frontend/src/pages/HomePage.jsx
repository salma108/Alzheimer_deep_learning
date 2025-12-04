import React from "react";
import { Link } from "react-router-dom";
import Card from "../components/Card";

function HomePage() {
  return (
    <div className="page page-centered">
      <div className="home-hero">
        <h1>Assistant IRM Alzheimer</h1>
        <p>
          Outil d’aide à la décision pour la détection des stades d’Alzheimer
          à partir d’images IRM, basé sur des modèles Deep Learning
          (ResNet50, DenseNet121, ViT).
        </p>
        <div className="home-actions">
          <Link to="/new-analysis" className="btn-primary">
            Commencer une analyse
          </Link>
          <Link to="/dashboard" className="btn-ghost">
            Voir le tableau de bord
          </Link>
        </div>
      </div>

      <div className="home-grid">
        <Card
          title="Analyse automatique"
          subtitle="Classification en 4 classes"
        >
          <ul className="home-list">
            <li>Non Demented</li>
            <li>Very Mild Demented</li>
            <li>Mild Demented</li>
            <li>Moderate Demented</li>
          </ul>
        </Card>

        <Card
          title="Explicabilité (XAI)"
          subtitle="Grad-CAM / Attention Rollout"
        >
          <p>
            Chaque prédiction est accompagnée d’une carte de chaleur montrant
            les zones les plus importantes pour la décision du modèle.
          </p>
        </Card>

        <Card
          title="Rapport médical"
          subtitle="PDF structuré pour le dossier patient"
        >
          <p>
            Le système génère un compte-rendu avec les probabilités, le modèle
            utilisé, les métadonnées patient et une synthèse textuelle.
          </p>
        </Card>
      </div>
    </div>
  );
}

export default HomePage;
