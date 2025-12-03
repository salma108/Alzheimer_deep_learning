import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { loginUser, saveAuth } from "../api/auth";

function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const data = await loginUser({ email, password });
      saveAuth(data);
      navigate("/dashboard");
    } catch (err) {
      alert(err.message || "Erreur de connexion");
    }
  }

  return (
    <div className="page auth-page">
      <div className="auth-card">
        <h2>Connexion</h2>
        <p className="auth-subtitle">
          Accédez à votre espace médecin et à vos analyses IRM.
        </p>
        <form onSubmit={handleSubmit} className="auth-form">
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
            Se connecter
          </button>
        </form>
        <p className="auth-switch">
          Pas encore de compte ? <Link to="/register">Créer un compte</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
