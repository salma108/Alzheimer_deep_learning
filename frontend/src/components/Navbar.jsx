import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { logout, loadAuth } from "../api/auth";

function Navbar() {
  const navigate = useNavigate();
  const auth = loadAuth();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header className="navbar">
      <div className="navbar-left">
        <span className="logo-dot" />
        <span className="logo-text">Alzheimer MRI Assistant</span>
      </div>
      <nav className="navbar-right">
        <Link to="/">Accueil</Link>

        {auth && (
          <>
            <Link to="/dashboard">Tableau de bord</Link>
            <Link to="/new-analysis">Nouvelle analyse</Link>
            <Link to="/history">Historique</Link>
          </>
        )}

        {!auth ? (
          <>
            <Link to="/login">Connexion</Link>
            <Link to="/register" className="btn-primary small">
              S'inscrire
            </Link>
          </>
        ) : (
          <button onClick={handleLogout} className="btn-ghost small">
            Déconnexion
          </button>
        )}
      </nav>
    </header>
  );
}

export default Navbar;
