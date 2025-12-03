import React from "react";
import { useLocation, Link, useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import Card from "../components/Card";
import ProbabilityBar from "../components/ProbabilityBar";
import XAIViewer from "../components/XAIViewer";

function generateTextSummary(prediction, probabilities) {
  if (!prediction || !probabilities) return "";
  const mainProb = (probabilities[prediction] * 100).toFixed(1);
  return `Le modèle estime que le patient est le plus probablement dans la classe "${prediction}" avec une probabilité de ${mainProb}%. Ce résultat doit être interprété en complément de l'examen clinique et d'autres examens radiologiques.`;
}

function ResultPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const result = location.state?.result;

  if (!result) {
    return (
      <div className="page page-centered">
        <p>Aucun résultat à afficher.</p>
        <button
          onClick={() => navigate("/new-analysis")}
          className="btn-primary"
        >
          Lancer une analyse
        </button>
      </div>
    );
  }

  const { model, prediction, probabilities, xai, report_pdf, patient } = result;
  const summary = generateTextSummary(prediction, probabilities);

  return (
    <div className="page with-sidebar">
      <Sidebar />
      <main className="page-content">
        <h1>Résultat de l'analyse</h1>
        <p className="page-subtitle">
          Synthèse automatique générée par le meilleur modèle entraîné.
        </p>

        <div className="grid-2">
          <Card title="Diagnostic synthétique">
            <p className="result-diagnosis">{prediction}</p>
            <p className="result-model">Modèle utilisé : {model}</p>
            {patient && (
              <p className="result-patient">
                Patient : {patient.name || "Inconnu"}{" "}
                {patient.age && `• ${patient.age} ans`}{" "}
                {patient.sex && `• ${patient.sex}`}
              </p>
            )}
            <p className="result-text">{summary}</p>
            <a
              href={report_pdf}
              target="_blank"
              rel="noreferrer"
              className="btn-ghost"
            >
              Ouvrir le rapport PDF complet
            </a>
          </Card>

          <Card title="Probabilités par classe">
            <ProbabilityBar
              probabilities={probabilities}
              highlight={prediction}
            />
          </Card>
        </div>

        <XAIViewer xaiBase64={xai} />

        <div className="result-actions">
          <Link to="/new-analysis" className="btn-primary">
            Analyser une nouvelle IRM
          </Link>
          <Link to="/history" className="btn-ghost">
            Voir l'historique
          </Link>
        </div>
      </main>
    </div>
  );
}

export default ResultPage;
