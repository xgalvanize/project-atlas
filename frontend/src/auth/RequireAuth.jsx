import React from "react";
import LoginPage from "./LoginPage";

export default function RequireAuth({ children }) {
  const token = localStorage.getItem("token");

  if (!token) {
    return <LoginPage />;
  }

  return children;
}
