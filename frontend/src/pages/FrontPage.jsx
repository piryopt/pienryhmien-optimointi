import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

const FrontPage = () => {
  const { t } = useTranslation();

  return (
    <div>
      <div>
        <Link to="/surveys/create">
          {t(
            "Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta"
          )}
        </Link>
      </div>
      <div>
        <Link to="/multistage/survey/create">
          {t(
            "Luo uusi monivaiheinen kysely, jossa määritetään eri vaiheiden vastausvaihtoehdot"
          )}
        </Link>
      </div>
      <div>
        <Link to="/surveys">{t("Näytä vanhat kyselyt")}</Link>
      </div>
    </div>
  );
};

export default FrontPage;
