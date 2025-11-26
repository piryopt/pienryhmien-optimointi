import { useTranslation } from "react-i18next";
import Table from "../Table";
import SurveyTableRow from "./SurveyTableRow";
import surveyService from "../../services/surveys";
import { useNotification } from "../../context/NotificationContext";
import { useSurveyDialog } from "../../context/SurveyDialogContext";
import { imagesBaseUrl } from "../../utils/constants";

const SurveysTable = ({ surveys, setSurveys }) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const { openDialog } = useSurveyDialog();

  const handleDeleteClick = async (surveyId) => {
    openDialog(
      t("Poista kysely?"),
      t(
        "Haluatko siirtää kyselyn roskakoriin? Avoimet kyselyt samalla suljetaan."
      ),
      surveyId,
      async () => {
        try {
          await surveyService.trashSurvey(surveyId);
          setSurveys((prev) => prev.filter((s) => s.id !== surveyId));
          showNotification(t("Kysely siirretty roskakoriin"), "success");
        } catch (err) {
          showNotification(
            t("Kyselyn siirto roskakoriin epäonnistui"),
            "error"
          );
          console.error("Error trashing survey:", err);
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
      title: t("Vastausaika päättyy"),
      icon: `${imagesBaseUrl}/schedule_white_36dp.svg`
    }
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
