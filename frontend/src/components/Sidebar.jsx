import React from "react";
import { NavLink } from "react-router-dom";

function Sidebar() {
  return (
    <aside className="sidebar">
      <h3 className="sidebar-title">Navigation</h3>
      <nav className="sidebar-nav">
        <NavLink to="/dashboard" className="sidebar-link">
          Aperçu global
        </NavLink>
        <NavLink to="/new-analysis" className="sidebar-link">
          Nouvelle IRM
        </NavLink>
        <NavLink to="/history" className="sidebar-link">
          Historique
        </NavLink>
      </nav>
    </aside>
  );
}

export default Sidebar;
