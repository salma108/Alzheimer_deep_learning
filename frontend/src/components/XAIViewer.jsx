import React from "react";
import Card from "./Card";

function XAIViewer({ xaiBase64 }) {
  if (!xaiBase64) return null;

  return (
    <Card
      title="Explication visuelle (XAI)"
      subtitle="Heatmap superposée à l’IRM"
    >
      <img
        src={`data:image/png;base64,${xaiBase64}`}
        alt="XAI"
        className="xai-image"
      />
    </Card>
  );
}

export default XAIViewer;
