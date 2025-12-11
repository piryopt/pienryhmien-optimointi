import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthProvider";
import { useNavigate } from "react-router-dom";
import { useNotification } from "../context/NotificationContext";
import { imagesBaseUrl } from "../utils/constants";
import { useEffect, useState } from "react";
import { baseUrl } from "../utils/constants";

const Navbar = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const { loading, logout, debug } = useAuth();
  const [displayName, setDisplayName] = useState("");
  const navigate = useNavigate();

  const handleLogout = async (e) => {
    e?.preventDefault();

    if (debug) {
      await logout();
      showNotification(t("Kirjautuminen ulos onnistui"), "success");
      navigate("/");
    } else {
      window.location.replace("/api/logout");
    }
  };
  const fetchSession = async () => {
    const res = await fetch(`${baseUrl}/session`, {
      credentials: "include"
    });
    const data = await res.json();
    setDisplayName(data.logged_in ? data.full_name : "");
  };
  useEffect(() => {
    fetchSession();
  }, []);

  return (
    <nav className="navbar navbar-expand-lg navbar-dark">
      <div className="container-fluid">
        <a className="navbar-brand" href="/">
          <img
            src={`${imagesBaseUrl}/hy_logo.svg`}
            alt=""
            width="34"
            height="30"
            className="d-inline-block align-text-top"
          />
          {t("Jakaja")}
        </a>

        <div className="d-flex">
          <div className="dropdown" style={{ marginRight: "55px" }}>
            <button
              className="btn dropdown btn-sm"
              type="button"
              id="dropdownMenuButton1"
              data-bs-toggle="dropdown"
              aria-expanded="false"
            >
              <b> {loading ? "" : displayName}</b>
            </button>
            <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton1">
              <li>
                <a className="dropdown-item" href="#" onClick={handleLogout}>
                  <small>{t("Kirjaudu ulos")}</small>
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
