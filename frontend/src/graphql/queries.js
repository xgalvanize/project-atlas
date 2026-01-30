import { gql } from "@apollo/client";

export const GET_PROJECTS = gql`
  query {
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
          createdBy {
            username
          }
        }
      }
    }
  }
`;