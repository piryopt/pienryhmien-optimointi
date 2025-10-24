import { useTranslation } from "react-i18next";
import Table from "../Table";
import SurveyTableRow from "./SurveyTableRow";
import assignmentWhite from "/images/assignment_white_36dp.svg";
import toggleOnWhite from "/images/toggle_on_white_36dp.svg";
import toggleOffWhite from "/images/toggle_off_white_36dp.svg";
import scheduleWhite from "/images/schedule_white_36dp.svg";
import menuWhite from "/images/menu_white_36dp.svg";
import surveyService from "../../services/surveys";

const SurveysTable = ({
  activeSurveys,
  closedSurveys,
  setActiveSurveys,
  setClosedSurveys
}) => {
  const { t } = useTranslation();

  const handleDeleteClick = async (surveyId, closedStatus) => {
    if (window.confirm(t("Haluatko varmasti poistaa kyselyn?"))) {
      try {
        await surveyService.deleteSurvey(surveyId);
        if (closedStatus)
          setClosedSurveys((prev) => prev.filter((s) => s.id !== surveyId));
        else setActiveSurveys((prev) => prev.filter((s) => s.id !== surveyId));
      } catch (err) {
        console.error("Error deleting survey:", err);
      }
    }
  };

  const allSurveys = [...activeSurveys, ...closedSurveys];
  const columns = [
    { title: t("Kysely"), logo: assignmentWhite },
    { title: t("Kyselyn tila"), logo: toggleOnWhite },
    { title: t("Ryhmät luotu"), logo: toggleOffWhite },
    { title: t("Toiminnot"), logo: menuWhite, style: { minWidth: "22em" } },
    { title: t("Vastausaika päättyy"), logo: scheduleWhite }
  ];

  return (
    <Table
      columns={columns}
      data={allSurveys}
      renderRow={(survey, i) => (
        <SurveyTableRow
          key={i}
          survey={survey}
          handleDeleteClick={handleDeleteClick}
        />
      )}
    />
  );
};

export default SurveysTable;
