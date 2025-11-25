import { useTranslation } from "react-i18next";

const MinChoicesSection = ({ choices, survey, multistage = false }) => {
  const { t } = useTranslation();

  const choicesAmount = choices?.length ?? 0;
  const minChoices = survey?.min_choices ?? 0;
  const allRequired = minChoices === choicesAmount;

  const minChoicesPerStage = multistage
    ? Object.values(survey.min_choices_per_stage).map((v) => Number(v))
    : null;

  const choiceAmountsPerStage = multistage
    ? choices.map((c) => c.choices.length)
    : null;

  // checks if in each stage min choices amount equals stage choices amount
  const allRequired2 = multistage
    ? minChoicesPerStage.length === choiceAmountsPerStage.length &&
      minChoicesPerStage.every((v, i) => v === choiceAmountsPerStage[i])
    : null;

  const showMinChoicesSection = !multistage
    ? minChoices !== choicesAmount
    : !allRequired2;

  const minChoicesValue = !multistage
    ? minChoices
    : (minChoicesPerStage[0] ?? "");

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
            checked={!multistage ? allRequired : allRequired2}
            readOnly
            disabled={!multistage ? !allRequired : !allRequired2}
          />
          <label htmlFor="min-choices-all">{t("Kyllä")}</label>
          <input
            type="radio"
            id="min-choices-custom"
            checked={!multistage ? !allRequired : !allRequired2}
            readOnly
            disabled={!multistage ? allRequired : allRequired2}
          />
          <label htmlFor="min-choices-custom">{t("Ei")}</label>
        </div>

        {showMinChoicesSection && (
          <div className="min-choices-section">
            <label htmlFor="minchoices" className="input-label">
              {t("Priorisoitujen ryhmien vähimmäismäärä")}
            </label>
            <input
              type="number"
              id="minchoices"
              className="form-control"
              value={minChoicesValue}
              readOnly
            />
          </div>
        )}
      </section>
    </div>
  );
};

export default MinChoicesSection;
