import React from "react";

function Loader({ text = "Analyse en cours..." }) {
  return (
    <div className="loader-wrapper">
      <div className="spinner" />
      <p>{text}</p>
    </div>
  );
}

export default Loader;
