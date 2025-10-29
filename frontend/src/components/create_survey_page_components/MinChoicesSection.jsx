import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const MinChoicesSection = () => {
  const { register, watch } = useFormContext();
  const { t } = useTranslation();

  const setting = watch("minChoicesSetting", "all");

  return (
    <section>
      <div>
        <h3>{t("Vaaditaanko kaikkien ryhmien järjestämistä?")}</h3>
        <p>
          {t(
            "Suositellaan, että vaaditaan kaikkien ryhmien järjestämistä ellei niitä ole suuri määrä (>10)"
          )}
        </p>

        <input
          type="radio"
          id="min-choices-all"
          {...register("minChoicesSetting")}
          value="all"
          defaultChecked
        />
        <label htmlFor="min-choices-all">{t("Kyllä")}</label>

        <input
          type="radio"
          id="min-choices-custom"
          {...register("minChoicesSetting")}
          value="custom"
        />
        <label htmlFor="min-choices-custom">{t("Ei")}</label>
      </div>

      {setting === "custom" && (
        <div className="min-choices-section">
          <label htmlFor="minchoices">
            {t("Priorisoitujen ryhmien vähimmäismäärä")}
          </label>
          <input
            type="number"
            id="minchoices"
            className="form-control"
            {...register("minchoices")}
            min={0}
          />
        </div>
      )}
    </section>
  );
};

export default MinChoicesSection;
