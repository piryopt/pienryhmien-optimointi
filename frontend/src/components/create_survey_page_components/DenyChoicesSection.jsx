import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const DenyChoicesSection = () => {
  const { register, watch } = useFormContext();
  const { t } = useTranslation();

  const setting = watch("denyChoicesSetting");

  return (
    <section>
      <div>
        <h3>{t("Sallitaanko valintojen kieltäminen?")}</h3>

        <input
          type="radio"
          id="deny-choices-yes"
          {...register("denyChoicesSetting")}
          value="show"
        />
        <label htmlFor="deny-choices-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="deny-choices-no"
          {...register("denyChoicesSetting")}
          value="hide"
        />
        <label htmlFor="deny-choices-no">{t("Ei")}</label>
      </div>

      {setting === "show" && (
        <div className="deny-choices-section">
          <label htmlFor="allowedDeniedChoices" className="input-label">
            {t("Sallittu kiellettyjen ryhmien määrä")}
          </label>
          <input
            type="number"
            id="allowedDeniedChoices"
            className="form-control"
            {...register("allowedDeniedChoices", { valueAsNumber: true })}
            min={0}
          />
        </div>
      )}
    </section>
  );
};

export default DenyChoicesSection;
