import { useTranslation } from "react-i18next";
import Table from "../Table";
import TrashTableRow from "./TrashTableRow";
import surveyService from "../../services/surveys";
import { useNotification } from "../../context/NotificationContext";
import assignmentIcon from "/images/assignment_white_36dp.svg";
import toggleOnIcon from "/images/toggle_on_white_36dp.svg";
import toggleOffIcon from "/images/toggle_off_white_36dp.svg";
import deleteDateIcon from "/images/auto_delete_36dp.svg";
import menuIcon from "/images/menu_white_36dp.svg";

const TrashTable = ({ surveys, setSurveys }) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();

  const handleDeleteClick = async (surveyId) => {
    if (
      window.confirm(
        t(
          "Haluatko varmasti poistaa kyselyn ja kaiken siihen liittyvän datan pysyvästi? "
        )
      )
    ) {
      try {
        //await surveyService.deleteSurvey(surveyId);
        //setSurveys((prev) => prev.filter((s) => s.id !== surveyId));
        console.log("Deleting survey...");
        showNotification(t("Kysely poistettu"), "success");
      } catch (err) {
        showNotification(t("Kyselyn poistaminen epäonnistui"), "error");
        console.error("Error deleting survey:", err);
      }
    }
  };

  const handleRestoreClick = async (surveyId) => {
    if (window.confirm(t("Haluatko palauttaa kyselyn roskakorista?"))) {
      try {
        console.log("Returning survey...");
        showNotification(t("Kysely palautettu"), "success");
      } catch (err) {
        showNotification(t("Kyselyn palauttaminen epäonnistui"), "error");
        console.error("Error restoring survey:", err);
      }
    }
  };

  const columns = [
    { title: t("Kysely"), icon: assignmentIcon },
    { title: t("Kyselyn tila"), icon: toggleOnIcon },
    { title: t("Ryhmät luotu"), icon: toggleOffIcon },
    { title: t("Toiminnot"), icon: menuIcon, style: { minWidth: "22em" } },
    { title: t("Kysely poistetaan"), icon: deleteDateIcon }
  ];

  return (
    <Table
      columns={columns}
      data={surveys}
      renderRow={(survey, i) => (
        <TrashTableRow
          key={i}
          survey={survey}
          handleDeleteClick={handleDeleteClick}
          handleRestoreClick={handleRestoreClick}
        />
      )}
    />
  );
};

export default TrashTable;
