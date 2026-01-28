import React, { useState } from "react";
import { useQuery, useMutation } from "@apollo/client/react";
import { gql } from "@apollo/client";

/* ----------------------------
   GraphQL Query: Get Projects
---------------------------- */
const GET_PROJECTS = gql`
  query GetProjects {
    projects {
      id
      name
      description
      createdAt
    }
  }
`;

/* ----------------------------
   GraphQL Mutation: Create Project
---------------------------- */
const CREATE_PROJECT = gql`
  mutation CreateProject($name: String!, $description: String) {
    createProject(name: $name, description: $description) {
      project {
        id
        name
        description
        createdAt
      }
    }
  }
`;

export default function ProjectsPage() {
  const { loading, error, data, refetch } = useQuery(GET_PROJECTS);

  const [createProject, { loading: creating }] =
    useMutation(CREATE_PROJECT);

  // Form state
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");

  async function handleCreate(e) {
    e.preventDefault();

    if (!name.trim()) return;

    await createProject({
      variables: {
        name,
        description,
      },
    });

    setName("");
    setDescription("");

    // Refresh project list
    refetch();
  }

  if (loading) return <p>Loading projects...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <h1>Projects</h1>

      {/* ----------------------
          Create Project Form
      ---------------------- */}
      <form
        onSubmit={handleCreate}
        style={{
          marginBottom: "2rem",
          padding: "1rem",
          border: "1px solid #ccc",
        }}
      >
        <h2>Create New Project</h2>

        <input
          style={{ width: "100%", marginBottom: "1rem" }}
          placeholder="Project name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />

        <textarea
          style={{ width: "100%", marginBottom: "1rem" }}
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />

        <button type="submit" disabled={creating}>
          {creating ? "Creating..." : "Create Project"}
        </button>
      </form>

      {/* ----------------------
          Project List
      ---------------------- */}
      <h2>Existing Projects</h2>

      {data.projects.length === 0 ? (
        <p>No projects yet.</p>
      ) : (
        <ul>
          {data.projects.map((p) => (
            <li key={p.id} style={{ marginBottom: "1rem" }}>
              <strong>{p.name}</strong>
              <p>{p.description}</p>
              <small>
                Created: {new Date(p.createdAt).toLocaleString()}
              </small>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
