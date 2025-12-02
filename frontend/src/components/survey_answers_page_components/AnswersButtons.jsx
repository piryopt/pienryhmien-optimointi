import { useTranslation } from "react-i18next";
import { useNotification } from "../../context/NotificationContext";
import { useNavigate } from "react-router-dom";
import surveyService from "../../services/surveys";
import { useSurveyDialog } from "../../context/SurveyDialogContext";
import SurveyDateOfClosing from "../create_survey_page_components/SurveyDateOfClosing";
import GroupSizesEditDialog from "./GroupSizesEditDialog";
import MultiStageGroupSizesEditDialog from "./MultiStageGroupSizesEditDialog";
import { FormProvider, useForm } from "react-hook-form";
import { format } from "date-fns";
import { buildCreateSurveySchema } from "../../utils/validations/createSurveyValidations";

const AnswersButtons = ({
  surveyClosed,
  setSurveyClosed,
  surveyId,
  surveyData,
  answers,
  multistage = false
}) => {
  const { t } = useTranslation("result");
  const { showNotification } = useNotification();
  const { openDialog, closeDialog } = useSurveyDialog();
  const navigate = useNavigate();

  const schema = buildCreateSurveySchema(t);

  const form = useForm({
    defaultValues: { enddate: null, endtime: "00:00" }
  });

  const handleOpenSurveyClick = async () => {
    openDialog(
      t("Avaa uudestaan?"),
      t("Haluatko varmasti avata kyselyn uudestaan?"),
      null,
      async () => {
        try {
          const data = form.getValues();
          await schema.validateAt("enddate", { enddate: data.enddate });
          await schema.validateAt("endtime", {
            enddate: data.enddate,
            endtime: data.endtime
          });
          const newEndDate = format(data.enddate, "dd.MM.yyyy");
          const newEndTime = data.endtime || "";
          await surveyService.openSurvey(surveyId, newEndDate, newEndTime);
          setSurveyClosed(false);
          showNotification(t("Kysely avattu"), "success");
        } catch (err) {
          showNotification(
            t(`Kyselyn avaaminen epäonnistui: ${err.message}`),
            "error"
          );
          console.error("error opening survey", err);
        }
      },
      <FormProvider {...form}>
        <SurveyDateOfClosing />
      </FormProvider>
    );
  };

  const handleCloseSurveyClick = async () => {
    openDialog(
      t("Sulje kysely?"),
      t("Haluatko varmasti sulkea kyselyn?"),
      null,
      async () => {
        try {
          await surveyService.closeSurvey(surveyId);
          setSurveyClosed(true);
          showNotification(t("Kysely suljettu"), "success");
        } catch (err) {
          console.error("error opening survey", err);
        }
      }
    );
  };

  const handleAssignGroups = () => {
    if (answers.length === 0) {
      showNotification(
        t("Ryhmäjakoa ei voida tehdä, sillä kyselyllä ei ole vastaajia"),
        "error"
      );
      return;
    } else if (!multistage && answers.length > surveyData.availableSpaces) {
      openDialog(
        t("Muokkaa ryhmäkokoja"),
        null,
        null,
        null,
        <GroupSizesEditDialog
          surveyId={surveyId}
          onClose={() => closeDialog()}
          onSuccess={() => {
            navigate(`/surveys/${surveyId}/results`);
          }}
          hideModalFooter={true}
        />
      );
      return;
    } else if (multistage) {
      surveyService.getMultiStageSurveyAnswersData(surveyId).then((data) => {
        const answers = data.answers || [];
        const available = data.availableSpaces || {};
        const answersCount = {};
        answers.forEach((obj) => {
          const key = Object.keys(obj)[0];
          const arr = obj[key] || [];
          answersCount[key] = arr.filter((a) => !a.notAvailable).length;
        });
        const stagesNeedingEdit = Object.keys(answersCount).filter((stage) => {
          const count = answersCount[stage] || 0;
          const avail = available[stage] || 0;
          return count > avail;
        });
        if (stagesNeedingEdit.length > 0) {
          openDialog(
            t("Muokkaa vaiheiden ryhmäkokoja"),
            null,
            null,
            null,
            <MultiStageGroupSizesEditDialog
              surveyId={surveyId}
              onClose={() => closeDialog()}
              onSuccess={() =>
                navigate(`/surveys/multistage/${surveyId}/results`)
              }
              hideModalFooter={true}
            />
          );
          return;
        } else {
          navigate(`/surveys/multistage/${surveyId}/results`);
          return;
        }
      });
      return;
    }
    if (multistage) {
      navigate(`/surveys/multistage/${surveyId}/results`);
      return;
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
