import { useTranslation } from "react-i18next";

const LimitParticipation = ({ survey, choices }) => {
  const { t } = useTranslation("create");

  // Collect participation_limit values from every stage choice
  const participationLimits =
    choices?.flatMap(
      (stage) =>
        stage?.choices?.map((c) => Number(c?.participation_limit ?? 0)) ?? []
    ) ?? [];

  // If all values are 0 (or there are no values) then no participation limit is set
  const hasParticipationLimit =
    participationLimits.length > 0 &&
    !participationLimits.every((v) => v === 0);

  return (
    <section>
      <div>
        <h3>{t("Rajoita osallistumiskertoja")}</h3>
        <p>
          {t(
            "Jos haluat rajoittaa kuinka monta kertaa vastaaja voi osallistua\
            johonkin ryhmään, vastaa tähän kyllä. Enimmäiskertojen määrän voit \
            myöhemmin asettaa jokaiselle ryhmälle vaiheen taulukossa. Jotta tämä \
            toimisi, tulee ryhmällä olla sama nimi kaikissa vaiheissa."
          )}
        </p>

        <input
          type="radio"
          id="limit-participation-yes"
          checked={hasParticipationLimit}
          readOnly
          disabled={!hasParticipationLimit}
        />
        <label htmlFor="limit-participation-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="limit-participation-no"
          checked={!hasParticipationLimit}
          readOnly
          disabled={hasParticipationLimit}
        />
        <label htmlFor="limit-participation-no">{t("Ei")}</label>
      </div>
    </section>
  );
};

export default LimitParticipation;
