// src/components/XAIViewer.jsx
import React from "react";
import Card from "./Card";

function XAIViewer({ xaiBase64 }) {
  if (!xaiBase64) return null;

  return (
    <Card
      title="Explication visuelle (XAI)"
      subtitle="Superposition de la heatmap sur l’IRM"
    >
      <div className="xai-wrapper">
        <img
          src={`data:image/png;base64,${xaiBase64}`}
          alt="XAI heatmap"
          className="xai-image"
        />
      </div>
    </Card>
  );
}

export default XAIViewer;
