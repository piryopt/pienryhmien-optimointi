import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const EditSurveyInfo = ({ placeholder }) => {
  const { register } = useFormContext();
  const { t } = useTranslation();

  return (
    <section>
      <h2>{t("Kyselyn kuvaus")}</h2>
      <p>
        {t(
          "Voit muokata kyselyn kuvausta"
        )}
      </p>
      <textarea
        id="survey-information"
        className="form-control"
        {...register("surveyInformation")}
        placeholder={placeholder}
      />
    </section>
  );
};

export default EditSurveyInfo;