import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthProvider";
import LoginPage from "../pages/LoginPage";

/**
 * RequireAdmin
 * - returns null while session is loading
 * - if not logged in -> behaves like RequireAuth
 * - if logged in but not admin -> redirects to front page ("/")
 * - otherwise renders children
 */
const RequireAdmin = ({ children }) => {
  const { user, loading, debug } = useAuth();

  if (loading) return null;

  if (!user || user.logged_in === false) {
    if (debug) {
      return <LoginPage />;
    }
    window.location.href = "/auth/login";
    return null;
  }

  if (!user.admin) {
    return <Navigate to="/" replace />;
  }

  return children;
};

export default RequireAdmin;
