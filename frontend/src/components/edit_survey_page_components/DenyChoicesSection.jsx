import { useTranslation } from "react-i18next";
const DenyChoicesSection = ({ survey }) => {
  const { t } = useTranslation();
  const a_d_c = survey.denied_allowed_choices;
  const denyAllowed = a_d_c !== 0;
  return (
    <section>
      <div>
        <h3>{t("Sallitaanko valintojen kieltäminen?")}</h3>

        <input
          type="radio"
          id="deny-choices-yes"
          checked={denyAllowed}
          readOnly
          disabled={!denyAllowed}
        />
        <label htmlFor="deny-choices-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="deny-choices-no"
          checked={!denyAllowed}
          readOnly
          disabled={denyAllowed}
        />
        <label htmlFor="deny-choices-no">{t("Ei")}</label>
      </div>

      {a_d_c !== 0 && (
        <div className="deny-choices-section">
          <label htmlFor="allowedDeniedChoices" className="input-label">
            {t("Sallittu kiellettyjen ryhmien määrä")}
          </label>
          <input
            type="number"
            id="allowedDeniedChoices"
            className="form-control"
            value={a_d_c}
            readOnly
          />
        </div>
      )}
    </section>
  );
};

export default DenyChoicesSection;
