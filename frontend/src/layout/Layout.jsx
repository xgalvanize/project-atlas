import React from "react";
import Navbar from "./Navbar";

export default function Layout({ children }) {
  return (
    <div>
      <Navbar />

      <main style={{ padding: "2rem" }}>
        {children}
      </main>
    </div>
  );
}
