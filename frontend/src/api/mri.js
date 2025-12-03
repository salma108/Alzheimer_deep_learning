// src/api/mri.js
import { loadAuth } from "./auth";

const API_BASE = "http://localhost:8000";

export async function analyzeMRI(file, formDataExtra = {}) {
  const auth = loadAuth();
  if (!auth || !auth.access_token) {
    throw new Error("Utilisateur non connecté");
  }

  const form = new FormData();
  form.append("file", file);

  Object.entries(formDataExtra).forEach(([k, v]) => {
    if (v != null) form.append(k, v);
  });

  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${auth.access_token}`,  // 🔥 IMPORTANT
    },
    body: form,
  });

  if (!res.ok) throw new Error("Erreur lors de l'analyse");

  return await res.json();
}
