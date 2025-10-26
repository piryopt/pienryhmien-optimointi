import hyLogo from "/images/hy_logo.svg";
import { useTranslation } from "react-i18next";
import { useAuth } from "../context/AuthProvider";
import { useNavigate } from "react-router-dom";
import { useNotification } from "../context/NotificationContext";

const Navbar = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const { user, loading, logout, debug } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async (e) => {
    e?.preventDefault();

    if (debug) {
      await logout();
      showNotification(t("Kirjautuminen ulos onnistui"), "success");
      navigate("/");
    } else {
      window.location.href = "/auth/logout";
    }
  };

  const displayName = user && user.full_name ? user.full_name : "";
  const isAdmin = !loading && user && user.admin;

  return (
    <nav className="navbar navbar-expand-lg navbar-dark">
      <div className="container-fluid">
        <a className="navbar-brand" href="/">
          <img
            src={hyLogo}
            alt=""
            width="34"
            height="30"
            className="d-inline-block align-text-top"
          />
          {t("Jakaja")}
        </a>
        {isAdmin && (
          <div className="collapse navbar-collapse" id="navbarNav">
            <a className="nav-link" href="#">
              <small>{t("Tilastot")}</small>
            </a>
            <a className="nav-link" href="#">
              <small>{t("Palaute")}</small>
            </a>
            <a className="nav-link" href="#">
              <small>{t("Aktiiviset kyselyt")}</small>
            </a>
          </div>
        )}

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
