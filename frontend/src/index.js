import React from "react";
import ReactDOM from "react-dom/client";
import { ApolloProvider } from "@apollo/client/react";
import { ApolloClient, InMemoryCache, HttpLink } from '@apollo/client';
import { setContext } from '@apollo/client/link/context';
import App from "./App";

const httpLink = new HttpLink({
  uri: "/graphql/",
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

const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache(),
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <ApolloProvider client={client}>
    <App />
  </ApolloProvider>
);


// import React from 'react';
// import ReactDOM from 'react-dom/client';
// import './index.css';
// import reportWebVitals from './reportWebVitals';

// import {
//   ApolloClient,
//   InMemoryCache,
//   ApolloProvider,
//   HttpLink
// } from "@apollo/client";
// import App from "./App";

// // Create a link to your GraphQL backend
// const link = new HttpLink({
//   uri: "http://127.0.0.1:8000/graphql/",
// });

// const client = new ApolloClient({
//   cache: new InMemoryCache(),
//   link: link,
// });

// const root = ReactDOM.createRoot(document.getElementById("root"));
// root.render(
//   <ApolloProvider client={client}>
//     <App />
//   </ApolloProvider>
// );


// // If you want to start measuring performance in your app, pass a function
// // to log results (for example: reportWebVitals(console.log))
// // or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
// reportWebVitals();
