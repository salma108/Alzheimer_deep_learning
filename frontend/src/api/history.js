import { loadAuth } from "./auth";

const API_BASE = "http://localhost:8000";

export async function fetchHistory() {
  const auth = loadAuth();
  if (!auth || !auth.access_token) {
    throw new Error("Utilisateur non connecté");
  }

  const res = await fetch(`${API_BASE}/history`, {
    headers: {
      Authorization: `Bearer ${auth.access_token}`,  // 🔥
    },
  });

  if (!res.ok) throw new Error("Impossible de récupérer l'historique");

  return await res.json();
}
