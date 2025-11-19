import { useTranslation } from "react-i18next";

const MinChoicesSection = ({ choices, survey }) => {
  const { t } = useTranslation();
  const choicesAmount = choices.length;
  const minChoices = survey.min_choices;
  const allRequired = minChoices === choicesAmount;
  return (
    <div>
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
            checked={allRequired}
            readOnly
            disabled={!allRequired}
          />
          <label htmlFor="min-choices-all">{t("Kyllä")}</label>
          <input
            type="radio"
            id="min-choices-custom"
            checked={!allRequired}
            readOnly
            disabled={allRequired}
          />
          <label htmlFor="min-choices-custom">{t("Ei")}</label>
        </div>

        {minChoices !== choicesAmount && (
          <div className="min-choices-section">
            <label htmlFor="minchoices" className="input-label">
              {t("Priorisoitujen ryhmien vähimmäismäärä")}
            </label>
            <input
              type="number"
              id="minchoices"
              className="form-control"
              value={minChoices}
              readOnly
            />
          </div>
        )}
      </section>
    </div>
  );
};

export default MinChoicesSection;
