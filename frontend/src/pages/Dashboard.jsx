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

export default function Dashboard() {
    const { loading, error, data, refetch } = useQuery(GET_PROJECTS);
    const [createProject] = useMutation(CREATE_PROJECT);
    const [createTask] = useMutation(CREATE_TASK);
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
                        <p key={t.id}>
                            {t.title} — {t.status}
                        </p>
                    ))}
                     <button onClick={() => handleCreateTask(p.id)}>
                        + Add Task
                    </button>
                </div>
            ))}
        </div>
    );
}