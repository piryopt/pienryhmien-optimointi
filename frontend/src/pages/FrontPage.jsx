import { useTranslation } from "react-i18next";

const FrontPage = () => {
  const { t } = useTranslation();

  return (
    <div>
      <div>
        <a href="/surveys/create">
          {t(
            "Luo uusi kysely tai tuo valmiit vastausvaihtoehdot csv-tiedostosta"
          )}
        </a>
      </div>
      <div>
        <a href="/multiphase/survey/create">
          {t(
            "Luo uusi monivaiheinen kysely, jossa määritetään eri vaiheiden vastausvaihtoehdot"
          )}
        </a>
      </div>
      <div>
        <a href="/surveys">{t("Näytä vanhat kyselyt")}</a>
      </div>
    </div>
  );
};

export default FrontPage;
