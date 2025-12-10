import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthProvider";
import { useNotification } from "../context/NotificationContext";

const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const { login, debug } = useAuth();
  const { showNotification } = useNotification();
  const navigate = useNavigate();
  const { t } = useTranslation();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await login({ username, password });
      showNotification(t("Kirjautuminen onnistui"), "success");
      //navigate("/"); // go to frontpage after login
    } catch (err) {
      showNotification(t("Kirjautuminen epäonnistui"), "error");
      console.error("Login failed", err);
    }
  };

  // if server debug is off, server handles the Haka login
  if (debug === false) {
    window.location.href = "/auth/login";
    return null;
  }

  return (
    <div>
      <h2>{t("Kirjaudu sisään")}</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>{t("Käyttäjätunnus")}:</label>
          <input
            type="text"
            name="username"
            data-testid="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>{t("Salasana")}:</label>
          <input
            type="password"
            name="password"
            data-testid="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit" data-testid="login-button">
          {t("Kirjaudu sisään")}
        </button>
      </form>
    </div>
  );
};

export default Login;
