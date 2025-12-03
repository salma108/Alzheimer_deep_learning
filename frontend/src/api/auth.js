const API_BASE = "http://localhost:8000";

export async function loginUser({ email, password }) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: email, password })
  });

  if (!res.ok) {
    throw new Error("Identifiants invalides");
  }
  return res.json();
}

export async function registerUser({ name, email, password }) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password })
  });

  if (!res.ok) {
    throw new Error("Erreur d'inscription");
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
