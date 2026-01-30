import { useState } from "react";
import InlineForm from "../InlineForm/InlineForm";

import ui from "../../styles/ui.module.css";
import styles from "./TaskItem.module.css";

export default function TaskItem({
    task,
    onStatusChange,
    onAddAction,
}) {
    const [showActionForm, setShowActionForm] = useState(false);

    return (
        <div className={styles.taskItem}>
            <div className={styles.row}>
                <div className={styles.title}>{task.title}</div>

                <div className={styles.controls}>
                    <select
                        className={ui.select}
                        value={task.status}
                        onChange={(e) => {
                            const newStatus = e.target.value;
                            onStatusChange(task.id, newStatus);
                        }}
                    >
                        <option value="PENDING">Pending</option>
                        <option value="IN_PROGRESS">In Progress</option>
                        <option value="DONE">Done</option>
                    </select>

                    <button
                        className={`${ui.button} ${ui.buttonOutline}`}
                        onClick={() => setShowActionForm(!showActionForm)}
                        type="button"
                    >
                        + Action
                    </button>
                </div>

            </div>

            {/* Inline Add Action Form */}
            {showActionForm && (
                <InlineForm
                    placeholder="New action description..."
                    buttonText="Add Action"
                    onSubmit={async (desc) => {
                        await onAddAction(task.id, desc);
                        setShowActionForm(false);
                    }}
                />
            )}

            {/* Actions List */}
            {task.actions.length > 0 && (
                <ul className={styles.actions}>
                    {task.actions.map((a) => (
                        <li key={a.id}>
                            {a.description} — {a.createdBy?.username}
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
