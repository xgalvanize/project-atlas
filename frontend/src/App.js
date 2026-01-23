import React from "react";
import { useQuery } from "@apollo/client/react";
import { gql } from "@apollo/client";
const GET_PROJECTS = gql`
  query {
    projects {
      id
      name
      actions {
        id
        actionType
        status
      }
    }
  }
`;

export default function App() {
  const { data, loading, error } = useQuery(GET_PROJECTS);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      {data.projects.map((project) => (
        <div key={project.id}>
          <h2>{project.name}</h2>
          <ul>
            {project.actions.map((action) => (
              <li key={action.id}>{action.actionType} - {action.status}</li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}
