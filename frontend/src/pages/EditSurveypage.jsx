import { useForm, FormProvider } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useTranslation } from "react-i18next";
import { buildEditSurveySchema } from "../utils/validations/editSurveyValidations";
import AddAdminSection from "../components/edit_survey_page_components/AddAdminSection";
import EditSurveyName from "../components/edit_survey_page_components/EditSurveyName";
import surveyService from "../services/surveys";
import { useEffect, useState, useMemo } from "react";
import { useParams, Link } from "react-router-dom";
import SurveyDateOfClosing from "../components/create_survey_page_components/SurveyDateOfClosing";
import { parse, format } from "date-fns";
import EditSurveyInfo from "../components/edit_survey_page_components/EditSurveyInfo";
import csrfService from "../services/csrf";
import { useNotification } from "../context/NotificationContext";
import { safeParseJson, extractMessage } from "../utils/parsers";
import { baseUrl } from "../utils/constants";

const EditSurveyPage = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();

  const schema = buildEditSurveySchema(t);
  const { id: surveyId } = useParams();
  const [survey, setSurvey] = useState(null);
  const [loading, setLoading] = useState(true);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      surveyName: ""
    },
    mode: "onBlur"
  });

  const parsedDeadline = useMemo(
    () =>
      survey?.deadline
        ? parse(survey.deadline, "dd.MM.yyyy HH:mm", new Date())
        : null,
    [survey]
  );

  useEffect(() => {
    if (!surveyId) return;
    let mounted = true;
    setLoading(true);
    const fetchSurvey = async () => {
      try {
        const response = await surveyService.getSurvey(surveyId);
        if (!mounted) return;
        setSurvey(response.survey);
        const parsed = response?.survey?.deadline
          ? parse(response.survey.deadline, "dd.MM.yyyy HH:mm", new Date())
          : null;
        methods.reset({
          surveyName: response?.survey.name,
          enddate: parsed,
          endtime: parsed ? format(parsed, "HH:mm") : "",
          adminEmail: ""
        });
        setLoading(false);
      } catch (error) {
        console.error("Error loading survey data:", error);
        if (mounted) setLoading(false);
      }
    };
    fetchSurvey();
    return () => {
      mounted = false;
    };
  }, [surveyId, methods]);

  const { handleSubmit } = methods;

  const onSubmit = async (data) => {
    console.log(data.enddate, data.endtime);
    const csrfToken = await csrfService.fetchCsrfToken();
    const updatedSurvey = {
      surveyGroupname: data.groupname,
      surveyInformation: data.surveyInformation,
      enddate: format(data.enddate, "dd.MM.yyyy"),
      endtime: data.endtime
    };

    try {
      const res = await fetch(`${baseUrl}/surveys/${surveyId}`, {
        method: "PATCH",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(updatedSurvey)
      });

      const json = await safeParseJson(res);
      if (!res.ok) {
        showNotification(
          extractMessage(json, res, t("Kyselyn muokkaus epäonnistui")),
          "error"
        );
        return;
      }
      if (!json || String(json.status) !== "1") {
        showNotification(
          extractMessage(json, res, t("Kyselyn muokkaus epäonnistui")),
          "error"
        );
        return;
      }
      showNotification(
        json.msg || t("Kysely muokattu onnistuneesti"),
        "success"
      );
    } catch (err) {
      showNotification(
        err?.message || t("Kyselyn muokkaus epäonnistui"),
        "error"
      );
    }
  };

  if (loading) {
    return <div>{t("Ladataan...")}</div>;
  }

  return (
    <div>
      <h1>{t("Kyselyn muokkaus")}</h1>
      <AddAdminSection surveyId={surveyId} />
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <EditSurveyName placeholder={survey.name} />
          <SurveyDateOfClosing
            placeholderDate={
              parsedDeadline ? format(parsedDeadline, "dd.MM.yyyy") : null
            }
            placeholderTime={
              parsedDeadline ? format(parsedDeadline, "HH:mm") : null
            }
          />
          <EditSurveyInfo placeholder={survey.description} />
          <button
            type="submit"
            className="btn btn-primary"
            style={{ marginRight: "25px" }}
          >
            {t("Tallenna muutokset")}
          </button>
          <Link className="btn btn-secondary" to="/surveys">
            {t("Palaa takaisin")}
          </Link>
        </form>
      </FormProvider>
    </div>
  );
};

export default EditSurveyPage;
