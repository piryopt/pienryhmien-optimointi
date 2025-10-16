import Navbar from "./Navbar";
import { useTranslation } from "react-i18next";
import LanguageSwitcher from "./LanguageSwitcher";

const SurveyMultiphaseCreate = () => {
  const { t } = useTranslation();

  return (
    <div>
      <Navbar />
      <LanguageSwitcher />
      <h1>{t("Luo uusi monivaiheinen kysely")}</h1>
      <p>{t("Tämä on kyselyn luontisivu!!")}</p>
    </div>
  );
};

export default SurveyMultiphaseCreate;
