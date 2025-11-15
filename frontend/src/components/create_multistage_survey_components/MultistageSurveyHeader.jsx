import { useTranslation } from "react-i18next";
import { imagesBaseUrl } from "../../utils/constants";

const MultistageSurveyHeader = () => {
  const { t } = useTranslation();
  return (
    <h1 className="page-title">
      <img
        src={`${imagesBaseUrl}/note_stack_add_36dp.svg`}
        alt="note add logo"
        className="d-inline-block align-text-middle"
      />
      {t("Luo uusi monivaiheinen kysely")}
    </h1>
  );
};

export default MultistageSurveyHeader;
