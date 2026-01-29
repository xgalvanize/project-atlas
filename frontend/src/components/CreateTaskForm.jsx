import React, { useState } from "react";
import { gql } from "@apollo/client";
import { useMutation } from "@apollo/client/react";
const CREATE_TASK = gql`
  mutation CreateTask($projectId: ID!, $title: String!, $description: String) {
    createTask(projectId: $projectId, title: $title, description: $description) {
      task {
        id
        title
        status
      }
    }
  }
`;

export default function CreateTaskForm({ projectId, onTaskCreated }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const [createTask, { loading, error }] = useMutation(CREATE_TASK);

  async function handleSubmit(e) {
    e.preventDefault();

    await createTask({
      variables: { projectId, title, description },
    });

    setTitle("");
    setDescription("");

    if (onTaskCreated) onTaskCreated();
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: "1rem" }}>
      <h3>Create Task</h3>

      <input
        placeholder="Task title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        style={{ width: "100%", marginBottom: "0.5rem" }}
      />

      <textarea
        placeholder="Description (optional)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        style={{ width: "100%", marginBottom: "0.5rem" }}
      />

      <button disabled={loading}>
        {loading ? "Creating..." : "Add Task"}
      </button>

      {error && <p style={{ color: "red" }}>{error.message}</p>}
    </form>
  );
}
