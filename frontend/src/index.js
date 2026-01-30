import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { AuthProvider } from "./auth/AuthContext";
import "./styles/globals.css";

import App from "./App";

import { ApolloProvider } from "@apollo/client/react";
import { client } from "./apolloClient";

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <ApolloProvider client={client}>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
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
