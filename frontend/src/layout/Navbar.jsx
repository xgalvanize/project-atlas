import React from "react";

export default function Navbar() {
  const token = localStorage.getItem("token");

  function handleLogout() {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    window.location.href = "/login";
  }

  return (
    <nav
      style={{
        padding: "1rem",
        background: "#222",
        color: "white",
        display: "flex",
        justifyContent: "space-between",
      }}
    >
      <h2>Project Atlas</h2>

      {token ? (
        <button onClick={handleLogout}>Logout</button>
      ) : (
        <span>Not logged in</span>
      )}
    </nav>
  );
}
