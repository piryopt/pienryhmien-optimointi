import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

const MultistageSurveyPrioritizedGroupsDescription = () => {
  const { t } = useTranslation("create");

  return (
    <section>
      <h2>{t("Priorisoitavat ryhmät")}</h2>
      <p>
        {t(
          "Syötä ryhmät, jotka kyselyyn vastaaja voi asettaa \
        mielekkyysjärjestykseen. Anna kullekkin ryhmälle myös sen enimmäiskoko. \
        Halutessasi voit lisätä lisätietoa kohteesta omiin sarakkeisiinsa. Sarakkeen \
        voit luoda painamalla '+ Lisää tietokenttä'."
        )}
      </p>
      <Link to="/csv-instructions" className="text-muted">
        {t("CSV-ohje")}
      </Link>
      <br />
      <br />
      <br />
      <p>
        {t(
          "Jos haluat, ettei jonkun tietyn sarakkeen tieto näy vastausvaiheessa \
            opiskelijoille, laita sen sarakkeen nimen viimeiseksi merkiksi *."
        )}
      </p>
      <p>
        {t(
          "Jos ryhmän minimikoolla ei ole väliä, syötä 0. Pakollisen ryhmän \
            mimimikoko ei voi olla 0."
        )}
      </p>
      <p>
        {t(
          "HUOM! Alle minimikoon jäävät ryhmät jätetään pois jaosta. Jos haluat, \
            että tietty ryhmä toteutuu varmasti, rastita ryhmän vasemmalla puolella \
            oleva laatikko."
        )}
      </p>
    </section>
  );
};

export default MultistageSurveyPrioritizedGroupsDescription;
