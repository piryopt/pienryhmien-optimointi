import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const SearchVisibilitySection = () => {
  const { setValue, watch } = useFormContext();
  const { t } = useTranslation();

  const value = watch("allowSearchVisibility", false);

  return (
    <section>
      <div>
        <h3>{t("Näytetäänkö vastaajalle hakupalkki?")}</h3>
        <p>
          {t(
            "Hakupalkin avulla kyselyyn vastaaja voi suodattaa näkemiään \
            vaihtoehtoja sen nimen ja vaihtoehtojen perusteella. Suositeltavaa sallia \
            kyselyille, joissa on runsaasti ei-pakollisia vaihtoehtoja, \
            ja vastaavasti kieltää pakollisia vaihtoehtoja sisältävälle \
            tai pienelle kyselylle."
          )}
        </p>

        <input
          type="radio"
          id="search-visibility-yes"
          name="allowSearchVisibility"
          checked={value === true}
          onChange={() => setValue("allowSearchVisibility", true)}
        />
        <label htmlFor="search-visibility-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="search-visibility-no"
          name="allowSearchVisibility"
          checked={value === false}
          onChange={() => setValue("allowSearchVisibility", false)}
        />
        <label htmlFor="search-visibility-no">{t("Ei")}</label>
      </div>
    </section>
  );
};

export default SearchVisibilitySection;
