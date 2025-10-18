import { useTranslation } from "react-i18next";
import finLogo from "../static/images/fin.svg";
import enLogo from "../static/images/eng.svg";
import swLogo from "../static/images/swe.svg";

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    localStorage.setItem("i18nextLng", lng);
  };

  return (
    <div className="language-switcher">
      <img
        src={finLogo}
        height={30}
        width={30}
        alt="Finnish flag"
        onClick={() => changeLanguage("fi")}
        style={{ cursor: "pointer" }}
      />
      <img
        src={enLogo}
        height={30}
        width={30}
        alt="British flag"
        onClick={() => changeLanguage("en")}
        style={{ cursor: "pointer" }}
      />
      <img
        src={swLogo}
        height={30}
        width={30}
        alt="Swedish flag"
        onClick={() => changeLanguage("sv")}
        style={{ cursor: "pointer" }}
      />
    </div>
  );
};

export default LanguageSwitcher;
