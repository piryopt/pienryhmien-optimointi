import { useTranslation } from "react-i18next";
import SurveyForm from "../components/create_survey_components/SurveyForm/SurveyForm";
import "../static/css/create_survey.css";

const CreateSurvey = () => {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t("Luo uusi kysely")}</h1>
      <SurveyForm />
    </div>
  );
};

export default CreateSurvey;