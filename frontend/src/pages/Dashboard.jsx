import React, { useState } from "react";
import ProjectsPage from "./ProjectsPage";
import { gql } from "@apollo/client";
import { useQuery, useMutation } from "@apollo/client/react";
import CreateTaskForm from "../components/CreateTaskForm";

const GET_PROJECTS = gql`
  query {
    projects {
      id
      name
      tasks {
        id
        title
        status
        actions {
          id
          description
          createdAt
          createdBy {
            username
          }
        }
      }
    }
  }
`;

const CREATE_PROJECT = gql`
  mutation CreateProject($name: String!) {
    createProject(name: $name) {
      project {
        id
        name
      }
    }
  }
`;
const CREATE_TASK = gql`
  mutation CreateTask($projectId: ID!, $title: String!) {
    createTask(projectId: $projectId, title: $title) {
      task {
        id
        title
        status
      }
    }
  }
`;

const UPDATE_TASK_STATUS = gql`
  mutation UpdateTaskStatus($taskId: ID!, $status: String!) {
    updateTaskStatus(taskId: $taskId, status: $status) {
      task {
        id
        status
      }
    }
  }
`;

const CREATE_ACTION = gql`
  mutation CreateAction($taskId: ID!, $description: String!) {
    createAction(taskId: $taskId, description: $description) {
      action {
        id
        description
        createdAt
        createdBy {
          username
        }
      }
    }
  }
`;

export default function Dashboard() {
    const { loading, error, data, refetch } = useQuery(GET_PROJECTS);
    const [createProject] = useMutation(CREATE_PROJECT);
    const [createTask] = useMutation(CREATE_TASK);
    const [updateTaskStatus] = useMutation(UPDATE_TASK_STATUS);
    const [createAction] = useMutation(CREATE_ACTION);
    const [projectName, setProjectName] = useState("");

    if (loading) return <p>Loading…</p>;
    if (error) return <p>Error: {error.message}</p>;

    async function handleCreateTask(projectId) {
        const title = prompt("Task title?");
        if (!title) return;

        await createTask({ variables: { projectId, title } });
        refetch();
    }

    async function handleCreateProject(e) {
        e.preventDefault();
        if (!projectName) return;

        await createProject({ variables: { name: projectName } });
        setProjectName("");
        refetch();
    }

    async function handleCreateAction(taskId) {
        const description = prompt("Action description?");
        if (!description) return;

        await createAction({ variables: { taskId, description } });
        refetch();
    }

    return (
        <div>
            <h1>Your Projects</h1>

            {/* Create Project Form */}
            <form onSubmit={handleCreateProject} style={{ marginBottom: "1rem" }}>
                <input
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="New project name"
                />
                <button type="submit">Create Project</button>
            </form>

            <hr />

            {/* List Projects */}
            {data.projects.map((p) => (
                <div key={p.id} style={{ marginBottom: "2rem" }}>
                    <h2>{p.name}</h2>

                    {p.tasks.map((t) => (
                        <div key={t.id} style={{ marginBottom: "1rem", paddingLeft: "1rem" }}>
                            <strong>{t.title}</strong>

                            <select
                                value={t.status}
                                onChange={async (e) => {
                                    await updateTaskStatus({
                                        variables: {
                                            taskId: t.id,
                                            status: e.target.value, // must be "PENDING", "IN_PROGRESS", "DONE"
                                        },
                                    });
                                    refetch();
                                }}
                            >
                                <option value="PENDING">Pending</option>
                                <option value="IN_PROGRESS">In Progress</option>
                                <option value="DONE">Done</option>
                            </select>


                            <button
                                onClick={() => handleCreateAction(t.id)}
                                style={{ marginLeft: "1rem" }}
                            >
                                + Add Action
                            </button>

                            {t.actions.length > 0 && (
                                <ul style={{ marginTop: "0.5rem" }}>
                                    {t.actions.map((a) => (
                                        <li key={a.id}>
                                            {a.description} — {a.createdBy?.username || "Unknown"} @{" "}
                                            {new Date(a.createdAt).toLocaleString()}
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    ))}

                    <button onClick={() => handleCreateTask(p.id)}>+ Add Task</button>
                </div>
            ))}
        </div>
    );
}