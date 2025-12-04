import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import Card from "../components/Card";
import ImageUploader from "../components/ImageUploader";
import Loader from "../components/Loader";
import { analyzeMRI } from "../api/mri";
import { useNavigate } from "react-router-dom";

function NewAnalysisPage() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [patientSex, setPatientSex] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      alert("Veuillez sélectionner une image IRM.");
      return;
    }
    setLoading(true);
    try {
      const result = await analyzeMRI(file, {
        patient_name: patientName || "Inconnu",
        patient_age: patientAge,
        patient_sex: patientSex,
        notes
      });
      navigate("/result", { state: { result } });
    } catch (err) {
      alert("Erreur lors de l'analyse.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page with-sidebar">
      <Sidebar />
      <main className="page-content">
        <h1>Nouvelle analyse IRM</h1>
        <p className="page-subtitle">
          Importez une IRM, complétez les informations patient et lancez
          l'analyse automatique.
        </p>

        <div className="grid-2">
          <Card title="Données patient">
            <div className="form-grid">
              <label>
                Nom du patient
                <input
                  type="text"
                  value={patientName}
                  onChange={(e) => setPatientName(e.target.value)}
                />
              </label>
              <label>
                Âge
                <input
                  type="number"
                  value={patientAge}
                  onChange={(e) => setPatientAge(e.target.value)}
                  placeholder="Ex : 68"
                />
              </label>
              <label>
                Sexe
                <select
                  value={patientSex}
                  onChange={(e) => setPatientSex(e.target.value)}
                >
                  <option value="">Non précisé</option>
                  <option value="F">Femme</option>
                  <option value="M">Homme</option>
                </select>
              </label>
              <label className="full">
                Notes cliniques
                <textarea
                  rows={4}
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Symptômes, historique, observations..."
                />
              </label>
            </div>
          </Card>

          <Card title="IRM à analyser">
            <ImageUploader onFileSelected={setFile} />
            <button
              className="btn-primary full"
              disabled={!file || loading}
              onClick={handleAnalyze}
            >
              Lancer l'analyse
            </button>
            {loading && <Loader />}
          </Card>
        </div>
      </main>
    </div>
  );
}

export default NewAnalysisPage;
