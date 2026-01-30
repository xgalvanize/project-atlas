import { useState } from "react";
import TaskItem from "../TaskItem/TaskItem";
import InlineForm from "../InlineForm/InlineForm";

import ui from "../../styles/ui.module.css";
import styles from "./ProjectCard.module.css";

export default function ProjectCard({
    project,
    onAddTask,
    onStatusChange,
    onAddAction,
}) {
    const [showTaskForm, setShowTaskForm] = useState(false);

    return (
        <div className={`${ui.card} ${styles.card}`}>
            <h2>{project.name}</h2>

            {/* Tasks */}
            {project.tasks.map((task) => (
                <TaskItem
                    key={task.id}
                    task={task}
                    onStatusChange={onStatusChange}
                    onAddAction={onAddAction}
                />
            ))}

            {/* Add Task Button */}
            <button
                className={`${ui.button} ${ui.buttonPrimary}`}
                onClick={() => setShowTaskForm(!showTaskForm)}
                type="button"
            >
                + Add Task
            </button>

            {/* Inline Add Task Form */}
            {showTaskForm && (
                <InlineForm
                    placeholder="New task title..."
                    buttonText="Create Task"
                    onSubmit={async (title) => {
                        await onAddTask(project.id, title);
                        setShowTaskForm(false);
                    }}
                />
            )}
        </div>
    );
}
