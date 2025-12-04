import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { registerUser, saveAuth } from "../api/auth";

function RegisterPage() {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const data = await registerUser({ name, email, password });
      saveAuth(data);
      navigate("/dashboard");
    } catch (err) {
      alert(err.message || "Erreur d'inscription");
    }
  }

  return (
    <div className="page auth-page">
      <div className="auth-card">
        <h2>Créer un compte</h2>
        <p className="auth-subtitle">Espace réservé au personnel médical.</p>
        <form onSubmit={handleSubmit} className="auth-form">
          <label>
            Nom / Prénom
            <input
              type="text"
              value={name}
              required
              onChange={(e) => setName(e.target.value)}
            />
          </label>
          <label>
            Email professionnel
            <input
              type="email"
              value={email}
              required
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>
          <label>
            Mot de passe
            <input
              type="password"
              value={password}
              required
              onChange={(e) => setPassword(e.target.value)}
            />
          </label>
          <button type="submit" className="btn-primary">
            Créer
          </button>
        </form>
        <p className="auth-switch">
          Déjà un compte ? <Link to="/login">Connexion</Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;
