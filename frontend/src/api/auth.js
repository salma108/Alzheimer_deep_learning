// frontend/src/api/auth.js

const API_BASE = "http://127.0.0.1:8000";

export async function loginUser({ email, password }) {
  // On prépare un vrai formulaire url-encodé pour FastAPI (OAuth2PasswordRequestForm)
  const form = new URLSearchParams();
  form.append("username", email);   // ⚠️ le backend attend "username"
  form.append("password", password);

  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: form.toString(),
  });

  if (!res.ok) {
    // On essaie de récupérer le message d'erreur du backend
    let detail = "Identifiants invalides";
    try {
      const data = await res.json();
      if (data?.detail) detail = data.detail;
    } catch (_) {}
    throw new Error(detail);
  }

  // Exemple de réponse : { access_token: "...", token_type: "bearer", user: {...} }
  return res.json();
}

export async function registerUser({ name, email, password }) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });

  if (!res.ok) {
    let detail = "Erreur d'inscription";
    try {
      const data = await res.json();
      if (data?.detail) detail = data.detail;
    } catch (_) {}
    throw new Error(detail);
  }

  return res.json();
}

export function saveAuth(data) {
  localStorage.setItem("auth", JSON.stringify(data));
}

export function loadAuth() {
  const raw = localStorage.getItem("auth");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export function logout() {
  localStorage.removeItem("auth");
}
