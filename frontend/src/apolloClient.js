import { ApolloClient, InMemoryCache, HttpLink } from "@apollo/client";
import { setContext } from "@apollo/client/link/context";
import { getToken, logout } from "./auth";
import { onError } from "@apollo/client/link/error";
const httpLink = new HttpLink({
  uri: "http://localhost:8000/graphql/",
});

const authLink = setContext((_, { headers }) => {
  const token = localStorage.getItem("token");
  return {
    headers: {
      ...headers,
      Authorization: token ? `JWT ${token}` : "",
    },
  };
});

export const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});

/* Auto logout if token expired */
// const errorLink = onError(({ graphQLErrors }) => {
//   if (graphQLErrors) {
//     graphQLErrors.forEach((err) => {
//       if (err.message.includes("Signature has expired")) {
//         alert("Session expired. Please log in again.");
//         logout();
//       }
//     });
//   }
// });

// export const client = new ApolloClient({
//   link: errorLink.concat(authLink.concat(httpLink)),
//   cache: new InMemoryCache(),
// });