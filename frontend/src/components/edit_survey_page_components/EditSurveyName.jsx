import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";
import "../../static/css/createSurveyPage.css";

const EditSurveyName = ({placeholder}) => {
  const { register, formState } = useFormContext();
  const { errors } = formState;
  const { t } = useTranslation();
  return (
    <section>
      <input type="hidden" id="edit_choices" value="True" />
      <h2>{t("Kyselyn nimi")}</h2>
      <input
        type="text"
        className="form-control"
        defaultValue={placeholder}
        {...register("groupname")}
        aria-invalid={!!errors.groupname}
        aria-describedby="groupname-validation-warning"
      />
      <ul className="validation-warnings-list">
        <li>
          <span
            className="input-validation-warning"
            id="groupname-validation-warning"
          >
            {errors.groupname?.message}
          </span>
        </li>
      </ul>
    </section>
  );
};

export default EditSurveyName;
