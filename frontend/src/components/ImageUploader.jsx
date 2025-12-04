import React, { useState } from "react";

function ImageUploader({ onFileSelected }) {
  const [preview, setPreview] = useState(null);

  const handleChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setPreview(URL.createObjectURL(file));
    onFileSelected(file);
  };

  return (
    <div className="uploader">
      <label className="uploader-label">
        Image IRM (JPG/PNG)
        <input type="file" accept="image/*" onChange={handleChange} />
      </label>
      {preview && (
        <div className="uploader-preview">
          <img src={preview} alt="IRM preview" />
        </div>
      )}
    </div>
  );
}

export default ImageUploader;
