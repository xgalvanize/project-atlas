import React from "react";
import { Routes, Route } from "react-router-dom";
import { useQuery, useMutation } from "@apollo/client/react";
import { gql } from "@apollo/client";
import Layout from "./components/Layout/Layout";
import RequireAuth from "./auth/RequireAuth";
import Dashboard from "./pages/Dashboard/Dashboard";
import LoginPage from "./auth/LoginPage";
// -----------------------------
// GraphQL Query
// -----------------------------

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

// -----------------------------
// GraphQL Mutation
// -----------------------------

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

const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    tokenAuth(username: $username, password: $password) {
      token
    }
  }
`;

// -----------------------------
// React Component
// -----------------------------

export default function App() {
  const { loading, error, data, refetch } = useQuery(GET_PROJECTS);

  const [updateTaskStatus] = useMutation(UPDATE_TASK_STATUS);

  if (loading) return <p>Loading projects…</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <Layout>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />
        <Route path="*" element={<LoginPage />} />
      </Routes>
    </Layout>
  );
}
//     <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
//       <h1>Project Atlas</h1>

//       {data.projects.map((project) => (
//         <div key={project.id} style={{ marginBottom: "2rem" }}>
//           <h2>{project.name}</h2>

//           {project.tasks.length === 0 ? (
//             <p>No tasks yet.</p>
//           ) : (
//             <ul>
//               {project.tasks.map((task) => (
//                 <li key={task.id}>
//                   <strong>{task.title}</strong>

//                   <br />

//                   Status:{" "}
//                   <select
//                     value={task.status}
//                     onChange={(e) => {
//                       updateTaskStatus({
//                         variables: {
//                           taskId: task.id,
//                           status: e.target.value,
//                         },
//                       }).then(() => refetch());
//                     }}
//                   >
//                     <option value="pending">pending</option>
//                     <option value="in_progress">in_progress</option>
//                     <option value="done">done</option>
//                   </select>
//                 </li>
//               ))}
//             </ul>
//           )}
//         </div>
//       ))}
//     </div>
//   );
// }


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
