import { useTranslation } from "react-i18next";

const AllowAbsencesSection = ({ survey }) => {
  const { t } = useTranslation("create");
  const allow_absences = survey.allow_absences;

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
          checked={allow_absences}
          readOnly
          disabled={!allow_absences}
        />
        <label htmlFor="allow-absences-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="allow-absences-no"
          checked={!allow_absences}
          readOnly
          disabled={allow_absences}
        />
        <label htmlFor="allow-absences-no">{t("Ei")}</label>
      </div>
    </section>
  );
};

export default AllowAbsencesSection;
