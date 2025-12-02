import { useTranslation } from "react-i18next";
import Table from "../Table";
import TrashTableRow from "./TrashTableRow";
import surveyService from "../../services/surveys";
import { useNotification } from "../../context/NotificationContext";
import { imagesBaseUrl } from "../../utils/constants";
import { useSurveyDialog } from "../../context/SurveyDialogContext";

const TrashTable = ({ surveys, setSurveys }) => {
  const { t } = useTranslation("list");
  const { showNotification } = useNotification();
  const { openDialog } = useSurveyDialog();

  const handleDeleteClick = async (surveyId) => {
    openDialog(
      t("Poista kaikki kyselyn data?"),
      t(
        "Haluatko varmasti poistaa kyselyn ja kaiken siihen liittyvän datan pysyvästi? "
      ),
      null,
      async () => {
        try {
          await surveyService.deleteSurvey(surveyId);
          setSurveys((prev) => prev.filter((s) => s.id !== surveyId));
          showNotification(t("Kysely poistettu"), "success");
        } catch (err) {
          showNotification(t("Kyselyn poistaminen epäonnistui"), "error");
          console.error("Error deleting survey:", err);
        }
      }
    );
  };

  const handleRestoreClick = async (surveyId) => {
    openDialog(
      t("Palauta kysely?"),
      t("Haluatko palauttaa kyselyn roskakorista?"),
      null,
      async () => {
        try {
          await surveyService.returnSurvey(surveyId);
          setSurveys((prev) => prev.filter((s) => s.id !== surveyId));
          showNotification(t("Kysely palautettu"), "success");
        } catch (err) {
          showNotification(t("Kyselyn palauttaminen epäonnistui"), "error");
          console.error("Error restoring survey:", err);
        }
      }
    );
  };

  const columns = [
    { title: t("Kysely"), icon: `${imagesBaseUrl}/assignment_white_36dp.svg` },
    {
      title: t("Kyselyn tila"),
      icon: `${imagesBaseUrl}/toggle_on_white_36dp.svg`
    },
    {
      title: t("Ryhmät luotu"),
      icon: `${imagesBaseUrl}/toggle_off_white_36dp.svg`
    },
    {
      title: t("Toiminnot"),
      icon: `${imagesBaseUrl}/menu_white_36dp.svg`,
      style: { minWidth: "22em" }
    },
    {
      title: t("Kysely poistetaan"),
      icon: `${imagesBaseUrl}/auto_delete_36dp.svg`
    }
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
