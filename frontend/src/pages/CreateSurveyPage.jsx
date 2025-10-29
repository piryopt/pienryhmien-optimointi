import { useState } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useTranslation } from "react-i18next";
import { useNotification } from "../context/NotificationContext";
import { buildCreateSurveySchema } from "../utils/validations/createSurveyValidations";
import { format } from "date-fns";
import csrfService from "../services/csrf";
import Header from "../components/create_survey_page_components/Header";
import SurveyNameInput from "../components/create_survey_page_components/SurveyNameInput";
import SurveyDateOfClosing from "../components/create_survey_page_components/SurveyDateOfClosing";
import "../static/css/createSurveyPage.css";

const CreateSurveyPage = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();

  const schema = buildCreateSurveySchema(t);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      groupname: "",
      enddate: null,
      endtime: "00:00",
      choices: [],
      minchoices: 1,
      surveyInformation: "",
      allowedDeniedChoices: [],
      allowSearchVisibility: false
    },
    mode: "onBlur"
  });

  const { handleSubmit } = methods;

  const onSubmit = async (data) => {
    const csrfToken = await csrfService.fetchCsrfToken();
    const payload = {
      surveyGroupname: data.groupname,
      surveyInformation: data.surveyInformation || "",
      choices: data.choices || [],
      minchoices: data.minchoices ?? 1,
      enddate: data.enddate ? format(data.enddate, "dd.MM.yyyy") : "",
      endtime: data.endtime || "",
      allowedDeniedChoices: data.allowedDeniedChoices || [],
      allowSearchVisibility: data.allowSearchVisibility || false
    };

    const extractMessage = (json, res) => {
      if (!json) return res?.statusText || t("Kyselyn luonti epäonnistui");
      if (typeof json === "string") return json;
      return (
        json.msg ||
        json.message ||
        res?.statusText ||
        t("Kyselyn luonti epäonnistui")
      );
    };

    try {
      const res = await fetch("http://localhost:5001/surveys/create", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(payload)
      });

      let json = null;
      try {
        json = await res.json();
      } catch {
        json = null;
      }

      if (!res.ok) {
        const msg = extractMessage(json, res);
        showNotification(msg, "error");
        return;
      }

      if (!json || String(json.status) !== "1") {
        const msg = extractMessage(json, res);
        showNotification(msg, "error");
        return;
      }

      showNotification(json.msg || t("Kysely luotu onnistuneesti"), "success");
    } catch (err) {
      showNotification(
        err?.message || t("Kyselyn luonti epäonnistui"),
        "error"
      );
    }
  };

  return (
    <div>
      <Header />
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <SurveyNameInput />
          <SurveyDateOfClosing />
          <button type="submit" className="btn btn-primary">
            {t("Luo kysely")}
          </button>
        </form>
      </FormProvider>
    </div>
  );
};

export default CreateSurveyPage;
