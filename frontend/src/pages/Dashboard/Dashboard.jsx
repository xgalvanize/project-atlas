import React, { useState } from "react";

import { useQuery, useMutation } from "@apollo/client/react";
// import CreateTaskForm from "../../components/CreateTaskForm";
import ProjectCard from "../../components/ProjectCard/ProjectCard";
import InlineForm from "../../components/InlineForm/InlineForm";
import styles from "./Dashboard.module.css";
import ui from "../../styles/ui.module.css";
import { GET_PROJECTS } from "../../graphql/queries";
import { CREATE_PROJECT, CREATE_TASK, CREATE_ACTION, UPDATE_TASK_STATUS } from "../../graphql/mutations";


export default function Dashboard() {
  const { loading, error, data, refetch } = useQuery(GET_PROJECTS);

  const [createProject] = useMutation(CREATE_PROJECT, {
    refetchQueries: [{ query: GET_PROJECTS }]
  });

  const [createTask] = useMutation(CREATE_TASK, {
    refetchQueries: [{ query: GET_PROJECTS }]
  });

  const [updateTaskStatus] = useMutation(UPDATE_TASK_STATUS, {
    refetchQueries: [{ query: GET_PROJECTS }]
  });

  const [createAction] = useMutation(CREATE_ACTION, {
    refetchQueries: [{ query: GET_PROJECTS }]
  });

  if (loading) return <p>Loading…</p>;
  if (error) return <p>Error: {error.message}</p>;

  async function handleAddTask(projectId, title) {
    await createTask({ variables: { projectId, title } });
  }

  async function handleAddAction(taskId, description) {
    await createAction({ variables: { taskId, description } });
  }

  async function handleStatusChange(taskId, status) {
    await updateTaskStatus({ variables: { taskId, status } });
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Your Projects</h1>
        <InlineForm
          placeholder="New project name..."
          buttonText="Create Project"
          onSubmit={async (name) => {
            await createProject({ variables: { name } });
            refetch();
          }}
        />
      </div>

      {data.projects.map((p) => (
        <ProjectCard
          key={p.id}
          project={p}
          onAddTask={handleAddTask}
          onStatusChange={handleStatusChange}
          onAddAction={handleAddAction}
        />
      ))}
    </div>
  );
}