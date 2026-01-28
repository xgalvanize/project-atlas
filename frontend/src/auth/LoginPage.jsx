import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@apollo/client/react";
import { gql } from "@apollo/client";
import { saveToken } from "../auth";


/* -----------------------------
   GraphQL Login Mutation
----------------------------- */
const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
      token
    }
  }
`;

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const [loginUser, { loading, error }] = useMutation(LOGIN);

 async function handleSubmit(e) {
    e.preventDefault();
    try {
      const result = await loginUser({ variables: { username, password } });

      localStorage.setItem("token", result.data.tokenAuth.token);
      localStorage.setItem(
        "refreshToken",
        result.data.tokenAuth.refreshToken
      );

      // Redirect after login
      navigate("/dashboard"); // <- useNavigate works now
    } catch (err) {
      console.error("Login failed:", err);
    }
  }

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <h1>Login to Atlas</h1>

      <form onSubmit={handleSubmit}>
        {/* Username */}
        <div style={{ marginBottom: "1rem" }}>
          <label>Username</label>
          <input
            style={{ width: "100%" }}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        {/* Password */}
        <div style={{ marginBottom: "1rem" }}>
          <label>Password</label>
          <input
            style={{ width: "100%" }}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        {/* Button */}
        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        {/* Error */}
        {error && (
          <p style={{ color: "red", marginTop: "1rem" }}>
            Error: {error.message}
          </p>
        )}
      </form>
    </div>
  );
}
