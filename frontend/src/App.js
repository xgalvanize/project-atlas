import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import RequireAuth from "./auth/RequireAuth";
import Dashboard from "./pages/Dashboard/Dashboard";
import LoginPage from "./auth/LoginPage";
import Layout from "./components/Layout/Layout";

export default function App() {
  return (
    <Layout>
      <Routes>
        {/* Public */}
        <Route path="/login" element={<LoginPage />} />

        {/* Protected */}
        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />

        {/* Default */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Layout>
  );
}

