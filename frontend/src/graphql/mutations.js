import { gql } from "@apollo/client";

export const CREATE_PROJECT = gql`
  mutation ($name: String!) {
    createProject(name: $name) {
      project {
        id
        name
        tasks {
          id
        }
      }
    }
  }
`;

export const CREATE_TASK = gql`
  mutation ($projectId: ID!, $title: String!) {
    createTask(projectId: $projectId, title: $title) {
      task {
        id
        title
        status
        createdBy {
          username
        }
        actions {
          id
        }
      }
    }
  }
`;

export const CREATE_ACTION = gql`
  mutation ($taskId: ID!, $description: String!) {
    createAction(taskId: $taskId, description: $description) {
      action {
        id
        description
        createdBy {
          username
        }
      }
    }
  }
`;

export const UPDATE_TASK_STATUS = gql`
  mutation ($taskId: ID!, $status: String!) {
    updateTaskStatus(taskId: $taskId, status: $status) {
      task {
        id
        status
      }
    }
  }
`;

