import { useTranslation } from "react-i18next";
import LanguageSwitcher from "./footer_components/LanguageSwitcher";
import { Link } from "react-router-dom";
import { imagesBaseUrl } from "../utils/constants";

const Footer = () => {
  const { t } = useTranslation();
  return (
    <footer className="footer mt-auto py-3 bg-dark">
      <div className="container">
        <Link to="/faq" className="text-muted">
          {t("UKK")}
        </Link>
        <Link to="/feedback" className="text-muted">
          {t("Anna palautetta")}
        </Link>
        <Link to="/user-manual" className="text-muted">
          {t("Käyttöohje")}
        </Link>
        <Link to="/privacy-policy" className="text-muted">
          {t("Tietosuojaseloste")}
        </Link>
        <LanguageSwitcher />
        <a href="https://github.com/piryopt/pienryhmien-optimointi">
          <img
            src={`${imagesBaseUrl}/github-mark-white.png`}
            alt="Jakaja GitHubissa"
            width="30"
            height="30"
          />
        </a>
      </div>
    </footer>
  );
};

export default Footer;
