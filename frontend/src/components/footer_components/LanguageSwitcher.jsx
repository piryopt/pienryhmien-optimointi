import { useState } from "react";
import { useTranslation } from "react-i18next";
import { languages } from "../utils/constants";

const LanguageSwitcher = () => {
  const [currLanguage, setCurrLanguage] = useState(localStorage.getItem("i18nextLng") || "fi");
  const { i18n } = useTranslation();
  
  const changeLanguage = (lng) => {
    setCurrLanguage(lng)
    i18n.changeLanguage(lng);
    localStorage.setItem("i18nextLng", lng);
  };

  return (
    <div className="language-switcher">
      {Object.keys(languages)
        .filter(language => language !== currLanguage)
        .map((language, i) => 
          <img 
            src={languages[language]["logo"]}
            height="30"
            width="30"
            alt={languages[language]["alt"]}
            onClick={() => changeLanguage(language)}
            style={{ cursor: "pointer" }}
            key={i}
          />
        )
      }
    </div>
  );
};

export default LanguageSwitcher;
