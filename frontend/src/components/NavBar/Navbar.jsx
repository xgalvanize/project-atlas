// src/layout/Navbar.jsx
import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";
import ui from "../../styles/ui.module.css";
import styles from "./Navbar.module.css";

export default function Navbar() {
  const { isLoggedIn, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); // clears token from context + localStorage
    navigate("/login"); // redirect to login page
  };

  return (
    <nav className={styles.nav}>
      <div className={styles.brand}>
        <Link to="/" className={styles.brandLink}>
          {/* logo removed */}
          <span className={styles.title}>Project Atlas</span>
        </Link>
      </div>

      <div className={styles.actions}>
        {isLoggedIn ? (
          <>
            <button
              onClick={handleLogout}
              className={`${ui.button} ${styles.logoutButton}`}
              type="button"
            >
              Logout
            </button>
          </>
        ) : (
          <Link to="/login" className={`${ui.button} ${ui.buttonPrimary} ${styles.navButton}`}>
            Login
          </Link>
        )}
      </div>
    </nav>
  );
}
