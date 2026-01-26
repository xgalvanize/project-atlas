import React from "react";
import { useQuery, useMutation } from "@apollo/client/react";
import { gql } from "@apollo/client";

// -----------------------------
// GraphQL Queries & Mutations
// -----------------------------

const GET_PROJECTS = gql`
  query GetProjects {
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
        }
      }
    }
  }
`;

const UPDATE_TASK_STATUS = gql`
  mutation UpdateTaskStatus($taskId: ID!, $status: String!) {
    updateTask(taskId: $taskId, status: $status) {
      task {
        id
        status
      }
    }
  }
`;

// -----------------------------
// React Component
// -----------------------------

export default function App() {
  const { loading, error, data, refetch } = useQuery(GET_PROJECTS);
  const [updateTaskStatus, { loading: updating, error: updateError }] =
    useMutation(UPDATE_TASK_STATUS);

  if (loading) return <p>Loading projects…</p>;
  if (error) return <p>Error loading projects: {error.message}</p>;

  return (
    <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
      <h1>Project Atlas</h1>

      {data.projects.map((project) => (
        <div key={project.id} style={{ marginBottom: "2rem" }}>
          <h2>{project.name}</h2>

          {project.tasks.length === 0 ? (
            <p>No tasks yet.</p>
          ) : (
            <ul>
              {project.tasks.map((task) => (
                <li key={task.id} style={{ marginBottom: "1rem" }}>
                  <strong>{task.title}</strong> — Status:{" "}
                  <select
                    value={task.status}
                    onChange={(e) => {
                      updateTaskStatus({
                        variables: {
                          taskId: task.id,
                          status: e.target.value,
                        },
                      }).then(() => {
                        refetch(); // refresh after update
                      });
                    }}
                  >
                    <option value="PENDING">PENDING</option>
                    <option value="IN_PROGRESS">IN_PROGRESS</option>
                    <option value="COMPLETED">COMPLETED</option>
                  </select>

                  {updating && <span> ⏳ Updating…</span>}
                  {updateError && (
                    <span style={{ color: "red" }}>
                      {" "}
                      Error: {updateError.message}
                    </span>
                  )}

                  {task.actions.length > 0 && (
                    <ul style={{ marginTop: "0.5rem", paddingLeft: "1rem" }}>
                      {task.actions.map((action) => (
                        <li key={action.id}>
                          {action.description} —{" "}
                          {new Date(action.createdAt).toLocaleString()}
                        </li>
                      ))}
                    </ul>
                  )}
                </li>
              ))}
            </ul>
          )}
        </div>
      ))}
    </div>
  );
}

// import React from "react";
// import { useQuery, useMutation } from "@apollo/client/react";
// import { gql } from "@apollo/client";


// // -----------------------------
// // GraphQL Queries & Mutations
// // -----------------------------

// const GET_PROJECTS = gql`
//   query GetProjects {
//     projects {
//       id
//       name
//       tasks {
//         id
//         title
//         status
//         actions {
//           id
//           description
//           createdAt
//         }
//       }
//     }
//   }
// `;

// const UPDATE_TASK_STATUS = gql`
//   mutation UpdateTaskStatus($taskId: ID!, $status: String!) {
//     updateTask(taskId: $taskId, status: $status) {
//       task {
//         id
//         status
//       }
//     }
//   }
// `;

// // -----------------------------
// // React Component
// // -----------------------------

// export default function App() {
//   const { data, loading, error } = useQuery(GET_PROJECTS);
//   const [updateTaskStatus] = useMutation(UPDATE_TASK_STATUS, {
//     refetchQueries: [GET_PROJECTS], // refresh tasks after status update
//   });

//   if (loading) return <p>Loading projects...</p>;
//   if (error) return <p>Error: {error.message}</p>;

//   return (
//     <div style={{ padding: "1rem", fontFamily: "sans-serif" }}>
//       <h1>Project Atlas</h1>
//       {data.projects.map((project) => (
//         <div key={project.id} style={{ marginBottom: "2rem" }}>
//           <h2>{project.name}</h2>
//           {project.tasks.length === 0 ? (
//             <p>No tasks yet.</p>
//           ) : (
//             <ul>
//               {project.tasks.map((task) => (
//                 <li key={task.id} style={{ marginBottom: "1rem" }}>
//                   <strong>{task.title}</strong> - Status:{" "}
//                   <select
//                     value={task.status}
//                     onChange={(e) =>
//                       updateTaskStatus({
//                         variables: {
//                           taskId: task.id,
//                           status: e.target.value,
//                         },
//                       })
//                     }
//                   >
//                     <option value="PENDING">PENDING</option>
//                     <option value="IN_PROGRESS">IN_PROGRESS</option>
//                     <option value="DONE">DONE</option>
//                   </select>

//                   {task.actions.length > 0 && (
//                     <ul style={{ marginTop: "0.5rem", paddingLeft: "1rem" }}>
//                       {task.actions.map((action) => (
//                         <li key={action.id}>
//                           {action.description} -{" "}
//                           {new Date(action.createdAt).toLocaleString()}
//                         </li>
//                       ))}
//                     </ul>
//                   )}
//                 </li>
//               ))}
//             </ul>
//           )}
//         </div>
//       ))}
//     </div>
//   );
// }
