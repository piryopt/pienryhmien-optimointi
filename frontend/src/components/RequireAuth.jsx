import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthProvider";
import LoginPage from "../pages/LoginPage";

const RequireAuth = ({ children }) => {
  const { user, loading, debug } = useAuth();

  // still loading session
  if (loading) return null; // or a spinner

  // user not logged in
  if (!user || user.logged_in === false) {
    if (debug) {
      return <LoginPage />;
    }
    // server handles Haka login
    window.location.href = "/auth/login";
    return null;
  }

  // logged in
  return children;
};

export default RequireAuth;
