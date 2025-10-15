import { useTranslation } from "react-i18next";

const fi = "/static/images/fin.svg";
const en = "/static/images/eng.svg";
const sv = "/static/images/swe.svg";

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
    localStorage.setItem("i18nextLng", lng);
  };

  return (
    <div>
      <img
        src={fi}
        height={30}
        width={30}
        alt="Finnish flag"
        onClick={() => changeLanguage("fi")}
      />
      <img
        src={en}
        height={30}
        width={30}
        alt="British flag"
        onClick={() => changeLanguage("en")}
      />
      <img
        src={sv}
        height={30}
        width={30}
        alt="Swedish flag"
        onClick={() => changeLanguage("sv")}
      />
    </div>
  );
};

export default LanguageSwitcher;
