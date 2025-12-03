// src/components/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";
import { loadAuth } from "../api/auth";

export default function ProtectedRoute({ children }) {
  const auth = loadAuth();
  if (!auth || !auth.access_token) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
