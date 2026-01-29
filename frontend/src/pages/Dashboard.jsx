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

export default function Dashboard() {
    const { loading, error, data, refetch } = useQuery(GET_PROJECTS);
    const [createProject] = useMutation(CREATE_PROJECT);
    const [createTask] = useMutation(CREATE_TASK);
    const [updateTaskStatus] = useMutation(UPDATE_TASK_STATUS);
    const [projectName, setProjectName] = useState("");


    if (loading) return <p>Loading…</p>;
    if (error) return <p>Error: {error.message}</p>;

    async function handleCreateTask(projectId) {
        const title = prompt("Task title?");
        if (!title) return;

        await createTask({
            variables: { projectId, title },
        });

        refetch();
    }

    async function handleCreateProject(e) {
        e.preventDefault();

        await createProject({
            variables: { name: projectName },
        });

        setProjectName("");
        refetch();
    }

    return (
        <div>
            <h1>Your Projects</h1>

            {/* Create Project Form */}
            <form onSubmit={handleCreateProject}>
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
                <div key={p.id}>

                    <h2>{p.name}</h2>

                    {p.tasks.map((t) => (
                        <div key={t.id} style={{ marginBottom: "0.5rem" }}>
                            <strong>{t.title}</strong>

                            <select
                                value={t.status}
                                onChange={async (e) => {
                                    await updateTaskStatus({
                                        variables: {
                                            taskId: t.id,
                                            status: e.target.value,
                                        },
                                    });
                                    refetch();
                                }}
                            >
                                <option value="PENDING">Pending</option>
                                <option value="IN_PROGRESS">In Progress</option>
                                <option value="DONE">Done</option>
                            </select>

                        </div>
                    ))}

                    <button onClick={() => handleCreateTask(p.id)}>
                        + Add Task
                    </button>
                </div>
            ))}
        </div>
    );
}