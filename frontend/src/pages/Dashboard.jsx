import React, { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";
import Card from "../components/Card";
import { fetchHistory } from "../api/history";

function Dashboard() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory()
      .then(setHistory)
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const total = history.length;
  const byClass = history.reduce((acc, h) => {
    acc[h.prediction] = (acc[h.prediction] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="page with-sidebar">
      <Sidebar />
      <main className="page-content">
        <h1>Tableau de bord</h1>
        <p className="page-subtitle">
          Synthèse des analyses IRM réalisées avec le système.
        </p>

        {loading ? (
          <p>Chargement...</p>
        ) : (
          <div className="grid-3">
            <Card title="Analyses réalisées">
              <p className="metric-main">{total}</p>
            </Card>
            <Card title="Répartition par diagnostic">
              {Object.keys(byClass).length === 0 ? (
                <p>Aucune analyse pour le moment.</p>
              ) : (
                <ul className="metric-list">
                  {Object.entries(byClass).map(([cls, n]) => (
                    <li key={cls}>
                      <strong>{cls}</strong> : {n}
                    </li>
                  ))}
                </ul>
              )}
            </Card>
            <Card title="Résumé projet">
              <p>
                Modèles comparés (ResNet50, DenseNet121, ViT), meilleur modèle
                déployé en production, XAI, rapport PDF médical et historique.
              </p>
            </Card>
          </div>
        )}
      </main>
    </div>
  );
}

export default Dashboard;
