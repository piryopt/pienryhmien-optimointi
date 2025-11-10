import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const AllowAbsencesSection = () => {
  const { register, watch } = useFormContext();
  const { t } = useTranslation();

  const value = watch("allowAbsences", false);

  return (
    <section>
      <div>
        <h3>{t("Sallitaanko poissaolot?")}</h3>
        <p>
          {t(
            "Salliessasi poissaolot, vastaajat voivat merkitä itsensä \
            poissaoleviksi valitsemistaan vaiheista."
          )}
        </p>

        <input
          type="radio"
          id="allow-absences-yes"
          value="true"
          {...register("allowAbsences", {
            setValueAs: (v) => v === "true"
          })}
        />
        <label htmlFor="allow-absences-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="allow-absences-no"
          value="false"
          {...register("allowAbsences", {
            setValueAs: (v) => v === "true"
          })}
          defaultChecked
        />
        <label htmlFor="allow-absences-no">{t("Ei")}</label>
      </div>
    </section>
  );
};

export default AllowAbsencesSection;
