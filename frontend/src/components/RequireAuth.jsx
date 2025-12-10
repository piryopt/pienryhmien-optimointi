import { useEffect } from "react";
import { useAuth } from "../context/AuthProvider";
import { useLocation, useNavigate } from "react-router-dom";
import LoginPage from "../pages/LoginPage";
const RequireAuth = ({ children }) => {
  const { user, loading, debug, refreshSession } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const redirect = async () => {
      if (!loading && user && user.logged_in) {
        await new Promise((resolve) => setTimeout(resolve, 10));

        const redirectTo = localStorage.getItem("redirectAfterLogin");
        if (redirectTo) {
          localStorage.removeItem("redirectAfterLogin");
          await refreshSession();
          window.location.replace(redirectTo);
        }
      }
    };
    redirect();
  }, [loading, user, refreshSession]);

  if (loading) return null;

  if (!user || user.logged_in === false) {
    if (debug) {
      return <LoginPage />;
    }
    // server handles Haka login
    localStorage.setItem("redirectAfterLogin", window.location.href);
  }

  return children;
};

export default RequireAuth;
