import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

/* -----------------------------
   Auth Provider
----------------------------- */
export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("token"));

  // ✅ Login stores token
  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  // ✅ Logout clears token
  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        login,
        logout,
        isLoggedIn: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

/* -----------------------------
   Hook
----------------------------- */
export const useAuth = () => useContext(AuthContext);
