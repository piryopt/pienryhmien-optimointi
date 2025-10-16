import githubLogo from "../static/images/github-mark-white.png";
import { useTranslation } from "react-i18next";
import LanguageSwitcher from "./LanguageSwitcher";

const Footer = () => {
  const { t } = useTranslation();
  return (
    <footer className="footer mt-auto py-3 bg-dark">
      <div className="container">
        <a href="#" className="text-muted">
          {t("UKK")}
        </a>
        <a href="#" className="text-muted">
          {t("Anna palautetta")}
        </a>
        <a href="#" className="text-muted">
          {t("Tietosuojaseloste")}
        </a>
        <LanguageSwitcher />
        <a href="https://github.com/piryopt/pienryhmien-optimointi">
          <img
            src={githubLogo}
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
