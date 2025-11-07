import { useTranslation } from "react-i18next";
import { useNotification } from "../../context/NotificationContext";
import { useNavigate } from "react-router-dom";
import surveyService from "../../services/surveys";

const AnswersButtons = ({
  surveyClosed,
  setSurveyClosed,
  surveyId,
  surveyData,
  answers
}) => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const navigate = useNavigate();

  const handleOpenSurveyClick = async () => {
    if (window.confirm(t("Haluatko varmasti avata kyselyn uudestaan?"))) {
      try {
        await surveyService.openSurvey(surveyId);
        setSurveyClosed(false);
        showNotification(t("Kysely avattu"), "success");
      } catch (err) {
        console.error("error opening survey", err);
      }
    }
  };

  const handleCloseSurveyClick = async () => {
    if (window.confirm(t("Haluatko varmasti sulkea kyselyn?"))) {
      try {
        await surveyService.closeSurvey(surveyId);
        setSurveyClosed(true);
        showNotification(t("Kysely suljettu"), "success");
      } catch (err) {
        console.error("error opening survey", err);
      }
    }
  };

  const handleAssignGroups = () => {
    if (answers.length === 0) {
      showNotification(
        t("Ryhmäjakoa ei voida tehdä, sillä kyselyllä ei ole vastaajia"),
        "error"
      );
      return;
    } else if (answers.length > surveyData.availableSpaces) {
      navigate(`/surveys/${surveyId}/group_sizes`);
    }
    navigate(`/surveys/${surveyId}/results`);
  };

  if (surveyClosed) {
    return (
      <div style={{ padding: "1em 0" }}>
        <button
          className="btn btn-outline-warning"
          style={{ float: "right" }}
          onClick={handleOpenSurveyClick}
        >
          {t("Avaa kysely uudelleen")}
        </button>
        <button
          className="btn btn-outline-primary"
          onClick={handleAssignGroups}
        >
          {t("Jaa ryhmiin")}
        </button>
      </div>
    );
  } else {
    return (
      <button
        className="btn btn-outline-warning"
        style={{ float: "right", zIndex: 2, position: "relative" }}
        onClick={handleCloseSurveyClick}
      >
        {t("Sulje kysely")}
      </button>
    );
  }
};

export default AnswersButtons;
