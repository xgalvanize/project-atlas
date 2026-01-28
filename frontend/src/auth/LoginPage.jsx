import React, { useState } from "react";
import { useMutation } from "@apollo/client/react";
import { gql } from "@apollo/client";

// -------------------
// GraphQL Login Mutation
// -------------------
const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
      token
      refreshToken
    }
  }
`;

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loginUser, { loading, error }] = useMutation(LOGIN);

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const result = await loginUser({
        variables: { username, password },
      });

      // Save tokens
      localStorage.setItem("token", result.data.tokenAuth.token);
      localStorage.setItem(
        "refreshToken",
        result.data.tokenAuth.refreshToken
      );

      // Redirect to dashboard
      window.location.href = "/";
    } catch (err) {
      console.error("Login failed:", err);
    }
  }

  return (
    <div style={{ maxWidth: "400px", margin: "2rem auto" }}>
      <h1>Login to Atlas</h1>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <label>Username</label>
          <input
            style={{ width: "100%" }}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <label>Password</label>
          <input
            style={{ width: "100%" }}
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        {error && (
          <p style={{ color: "red" }}>
            Error: {error.message}
          </p>
        )}
      </form>
    </div>
  );
}
