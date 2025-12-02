import React, { useEffect, useCallback } from "react";
import csrfService from "../../services/csrf";
import { useNotification } from "../../context/NotificationContext";
import { useForm, FormProvider } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useTranslation } from "react-i18next";
import { buildEditSurveyAdminSchema } from "../../utils/validations/editSurveyValidations.js";
import { safeParseJson, extractMessage } from "../../utils/parsers";
import { baseUrl } from "../../utils/constants.js";

const AddAdminSection = ({ value = "", onChange = () => {}, surveyId }) => {
  const { t } = useTranslation("create");
  const { showNotification } = useNotification();

  const schema = buildEditSurveyAdminSchema(t);

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      adminEmail: ""
    },
    mode: "onBlur"
  });

  const {
    register,
    handleSubmit,
    formState: { errors },
    watch,
    setValue
  } = methods;

  useEffect(() => {
    setValue("adminEmail", value || "");
  }, [value, setValue]);

  const watchedEmail = watch("adminEmail");
  useEffect(() => {
    onChange(watchedEmail);
  }, [watchedEmail, onChange]);

  const onSubmit = useCallback(
    async (data) => {
      try {
        const csrfToken = await csrfService.fetchCsrfToken();
        const res = await fetch(`${baseUrl}/surveys/${surveyId}/add_owner`, {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          },
          body: JSON.stringify({ email: data.adminEmail })
        });
        const json = await safeParseJson(res);
        if (!res.ok) {
          showNotification(
            extractMessage(
              json,
              res,
              t(
                `Hallinnointioikeuksien myöntäminen käyttäjälle ${watchedEmail} epäonnistui`
              )
            ),
            "error"
          );
          return;
        }
        if (!json || String(json.status) !== "1") {
          showNotification(
            extractMessage(
              json,
              res,
              t(
                `Hallinnointioikeuksien myöntäminen käyttäjälle ${watchedEmail} epäonnistui`
              )
            ),
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
    },
    [surveyId, showNotification, t, watchedEmail]
  );

  return (
    <div>
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)}>
          <h2>{t("Anna käyttäjälle hallinnointioikeudet kyselyyn.")}</h2>
          <p>{t("Syötä käyttäjän sähköpostiosoite.")}</p>

          <input
            type="text"
            className="form-control"
            placeholder={t("sähköpostiosoite")}
            {...register("adminEmail")}
          />

          <ul className="validation-warnings-list">
            <li>
              <span
                className="input-validation-warning"
                id="adminEmail-validation-warning"
              >
                {errors.adminEmail?.message}
              </span>
            </li>
          </ul>

          <button type="submit" className="btn btn-success">
            {t("Lisää käyttäjä")}
          </button>
        </form>
      </FormProvider>
    </div>
  );
};

export default React.memo(AddAdminSection);
