import { useTranslation } from "react-i18next";
import Table from "../Table";
import SurveyTableRow from "./SurveyTableRow";
import assignmentWhite from "/images/assignment_white_36dp.svg";
import toggleOnWhite from "/images/toggle_on_white_36dp.svg";
import toggleOffWhite from "/images/toggle_off_white_36dp.svg";
import scheduleWhite from "/images/schedule_white_36dp.svg";
import menuWhite from "/images/menu_white_36dp.svg";
import surveyService from "../../services/surveys";
import { useNotification } from "../../context/NotificationContext";
import { useSurveyDialog } from "../../context/SurveyDialogContext";

const SurveysTable = ({ surveys, setSurveys }) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const { openDialog } = useSurveyDialog();

  const handleDeleteClick = async (surveyId) => {
    openDialog(
      t("Poista kysely?"),
      t("Haluatko varmasti poistaa kyselyn?"),
      surveyId,
      async () => {
        try {
          await surveyService.trashSurvey(surveyId);
          setSurveys((prev) => prev.filter((s) => s.id !== surveyId));
          showNotification(t("Kysely poistettu"), "success");
        } catch (err) {
          showNotification(t("Kyselyn poistaminen epäonnistui"), "error");
          console.error("Error deleting survey:", err);
        }
      }
    );
  };

  const columns = [
    { title: t("Kysely"), icon: assignmentWhite },
    { title: t("Kyselyn tila"), icon: toggleOnWhite },
    { title: t("Ryhmät luotu"), icon: toggleOffWhite },
    { title: t("Toiminnot"), icon: menuWhite, style: { minWidth: "22em" } },
    { title: t("Vastausaika päättyy"), icon: scheduleWhite }
  ];

  return (
    <Table
      columns={columns}
      data={surveys}
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
