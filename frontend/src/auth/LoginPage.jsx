import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation, useApolloClient } from "@apollo/client/react";
import { gql } from "@apollo/client";
import { useAuth } from "./AuthContext";
import ui from "../styles/ui.module.css";
import styles from "./LoginPage.module.css";

/* -----------------------------
   GraphQL Login Mutation
----------------------------- */
const LOGIN = gql`
  mutation TokenAuth($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
      token
    }
  }
`;

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const { login } = useAuth();
  const navigate = useNavigate();
  const client = useApolloClient();

  const [loginUser, { loading, error }] = useMutation(LOGIN);

  async function handleSubmit(e) {
    e.preventDefault();

    try {
      const result = await loginUser({
        variables: { username, password },
      });

      const token = result.data.tokenAuth.token;

      // ✅ Save token in context + localStorage
      login(token);

      // ✅ Reset Apollo cache so queries rerun authenticated
      await client.resetStore();

      // ✅ Redirect
      navigate("/dashboard");
    } catch (err) {
      console.error("Login failed:", err);
    }
  }

  return (
    <div className={styles.container}>
      <div className={`${ui.card} ${styles.card}`}>
        <h1 className={styles.title}>Login to Atlas</h1>

        <form onSubmit={handleSubmit} className={styles.form}>
          <div className={styles.row}>
            <label>Username</label>
            <input
              className={ui.input}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className={styles.row}>
            <label>Password</label>
            <input
              className={ui.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className={`${ui.button} ${ui.buttonPrimary}`}
            >
              {loading ? "Logging in..." : "Login"}
            </button>
          </div>

          {error && (
            <p className={styles.error}>Error: {error.message}</p>
          )}
        </form>
      </div>
    </div>
  );
}
