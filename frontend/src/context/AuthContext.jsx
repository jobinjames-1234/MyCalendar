import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { fetchCsrf, getCurrentUser, loginUser, logoutUser } from "../api/authApi";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = async () => {
    try {
      const { data } = await getCurrentUser();
      setUser(data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchCsrf().finally(() => {});
    refreshUser();
  }, []);

  const handleLogin = async (payload) => {
    const { data } = await loginUser(payload);
    setUser(data.user);
    return data;
  };

  const handleLogout = async () => {
    await logoutUser();
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, loading, setUser, refreshUser, handleLogin, handleLogout }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
}
