// src/layout/Navbar.jsx
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Navbar() {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); // clears token from context + localStorage
    navigate("/login"); // redirect to login page
  };

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "1rem 2rem",
        backgroundColor: "#1E293B", // dark slate
        color: "#F8FAFC", // light text
        boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
      }}
    >
      <div style={{ fontWeight: "bold", fontSize: "1.5rem" }}>
        <Link to="/" style={{ color: "#F8FAFC", textDecoration: "none" }}>
          Project Atlas
        </Link>
      </div>

      <div>
        {isLoggedIn ? (
          <>
            <Link
              to="/dashboard"
              style={{
                marginRight: "1rem",
                color: "#F8FAFC",
                textDecoration: "none",
                fontWeight: "500",
              }}
            >
              Dashboard
            </Link>
            <button
              onClick={handleLogout}
              style={{
                padding: "0.5rem 1rem",
                backgroundColor: "#F87171", // red
                color: "#FFF",
                border: "none",
                borderRadius: "5px",
                cursor: "pointer",
                fontWeight: "500",
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <Link
            to="/login"
            style={{
              padding: "0.5rem 1rem",
              backgroundColor: "#3B82F6", // blue
              color: "#FFF",
              borderRadius: "5px",
              textDecoration: "none",
              fontWeight: "500",
            }}
          >
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}
