import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Card from "../components/Card";
import { fetchHistory } from "../api/history";

function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory()
      .then(setHistory)
      .catch(() => alert("Erreur lors du chargement de l'historique"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="page with-sidebar">
      <Sidebar />
      <main className="page-content">
        <h1>Historique des analyses</h1>
        <p className="page-subtitle">
          Liste chronologique des IRM analysées et rapports générés.
        </p>

        {loading ? (
          <p>Chargement...</p>
        ) : history.length === 0 ? (
          <p>Aucune analyse pour le moment.</p>
        ) : (
          <div className="history-table">
            <div className="history-header">
              <span>Date</span>
              <span>Patient</span>
              <span>Diagnostic</span>
              <span>Modèle</span>
              <span>Rapport</span>
            </div>
            {history.map((h) => (
              <div key={h.id} className="history-row">
                <span>
                  {new Date(h.created_at).toLocaleString("fr-FR", {
                    dateStyle: "short",
                    timeStyle: "short"
                  })}
                </span>
                <span>{h.patient?.name || "N/A"}</span>
                <span>{h.prediction}</span>
                <span>{h.model}</span>
                <span>
                  <a href={h.report} target="_blank" rel="noreferrer">
                    Ouvrir le PDF
                  </a>
                </span>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default HistoryPage;
