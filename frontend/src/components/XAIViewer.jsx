import React, { useState } from "react";
import Card from "./Card";
import "./xai.css";

function XAIViewer({ xaiBase64 }) {
  const [zoom, setZoom] = useState(false);

  if (!xaiBase64) return null;

  return (
    <>
      <Card title="Explication visuelle (XAI)"
            subtitle="Carte d'attention générée par Grad-CAM">
        
        <div className="xai-preview-container">
          <img
            src={`data:image/png;base64,${xaiBase64}`}
            alt="XAI heatmap"
            className="xai-preview"
            onClick={() => setZoom(true)}
          />
          <p className="xai-text">Cliquez sur l’image pour agrandir</p>
        </div>
      </Card>

      {/* OVERLAY ZOOM */}
      {zoom && (
        <div className="xai-overlay" onClick={() => setZoom(false)}>
          <img
            src={`data:image/png;base64,${xaiBase64}`}
            className="xai-zoom-image"
            alt="zoom heatmap"
          />
        </div>
      )}
    </>
  );
}

export default XAIViewer;
