import { useEffect } from "react";
import { useAuth } from "../context/AuthProvider";
import { useLocation, useNavigate } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
const RequireAuth = ({ children }) => {
  const { user, loading, debug, refreshSession } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  if (loading) return null;

  if (!user || user.logged_in === false) {
    localStorage.setItem(
      "redirectAfterLogin",
      location.pathname + location.search
    );

    const redirectTo = localStorage.getItem("redirectAfterLogin");
    if (redirectTo) {
      localStorage.removeItem("redirectAfterLogin");
      navigate(redirectTo);
    }
    if (debug) return <LoginPage />;
  }

  return children;
};

export default RequireAuth;
