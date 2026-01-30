import React, { useState } from "react";
import ProjectsPage from "../ProjectsPage";
import { gql } from "@apollo/client";
import { useQuery, useMutation } from "@apollo/client/react";
import CreateTaskForm from "../../CreateTaskForm";
import styles from "./Dashboard.module.css";
import ui from "../../../styles/ui.module.css";
const GET_PROJECTS = gql`
  query {
    projects {
      id
      name
      owner {
        username
      }
      tasks {
        id
        title
        status
        createdBy {
            username
        }
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
    //         await createAction({
    //   variables: { taskId, description },
    //   refetchQueries: ["GetProjects"],
    // });
    refetch();
  }

  return (
    <div className={styles.wrapper}>
      <h1>Your Projects</h1>

      {/* Create Project */}
      <form onSubmit={handleCreateProject} className={styles.formRow}>
        <input
          className={ui.input}
          value={projectName}
          onChange={(e) => setProjectName(e.target.value)}
          placeholder="New project name"
        />
        <button className={ui.button} type="submit">
          Create
        </button>
      </form>

      {/* Projects */}
      {data.projects.map((p) => (
        <div key={p.id} className={styles.projectCard}>
          <h2>{p.name}</h2>

          {/* Tasks */}
          {p.tasks.map((t) => (
            <div key={t.id}>
              <div className={styles.taskRow}>
                <span className={styles.taskTitle}>{t.title}</span>

                <select
                  className={ui.select}
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

                <button
                  className={`${ui.button} ${ui.buttonSecondary}`}
                  onClick={() => handleCreateAction(t.id)}
                >
                  + Action
                </button>
              </div>

              {/* Actions */}
              {t.actions.length > 0 && (
                <ul className={styles.actionsList}>
                  {t.actions.map((a) => (
                    <li key={a.id}>
                      {a.description} —{" "}
                      {a.createdBy?.username || "Unknown"}
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}

          <button
            className={ui.button}
            onClick={() => handleCreateTask(p.id)}
          >
            + Add Task
          </button>
        </div>
      ))}
    </div>
  );
}