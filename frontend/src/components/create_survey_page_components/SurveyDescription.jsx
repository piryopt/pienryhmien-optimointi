import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const SurveyDescription = () => {
  const { register } = useFormContext();
  const { t } = useTranslation();

  return (
    <section>
      <h2>{t("Kyselyn kuvaus")}</h2>
      <p>
        {t(
          "Tähän voit antaa kuvauksen kyselystä ja ohjeita siihen vastaamiseen. Kuvausteksti näytetään vastaajalle kyselyn yhteydessä."
        )}
      </p>
      <textarea
        id="survey-information"
        className="form-control"
        {...register("surveyInformation")}
      />
    </section>
  );
};

export default SurveyDescription;
