import React from "react";
import { useQuery, useMutation } from "@apollo/client/react";
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

const UPDATE_ACTION_STATUS = gql`
  mutation UpdateActionStatus($actionId: ID!, $status: String!) {
    updateActionStatus(actionId: $actionId, status: $status) {
      action {
        id
        status
      }
    }
  }
`;

export default function App() {
  const { data, loading, error } = useQuery(GET_PROJECTS);
  const [updateStatus] = useMutation(UPDATE_ACTION_STATUS);
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      {data.projects.map((project) => (
        <div key={project.id}>
          <h2>{project.name}</h2>
          <ul>
            {project.actions.map((action) => (
              <>
              <li key={action.id}>{action.actionType} - {action.status}</li>
              <select
  value={action.status}
  onChange={(e) => {
    updateStatus({
      variables: {
        actionId: action.id,
        status: e.target.value,
      },
    });
  }}
>
  <option value="pending">pending</option>
  <option value="in_progress">in_progress</option>
  <option value="completed">completed</option>
</select>
</>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}