import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const LimitParticipationSection = ({ setLimitParticipationVisible }) => {
  const { setValue, watch } = useFormContext();
  const { t } = useTranslation("create");

  const value = watch("limitParticipation", false);

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
          value="true"
          checked={value === true}
          onChange={() => {
            setValue("limitParticipation", true);
            setLimitParticipationVisible(true);
          }}
        />
        <label htmlFor="limit-participation-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="limit-participation-no"
          value="false"
          checked={value === false}
          onChange={() => {
            setValue("limitParticipation", false);
            setLimitParticipationVisible(false);
          }}
        />
        <label htmlFor="limit-participation-no">{t("Ei")}</label>
      </div>
    </section>
  );
};

export default LimitParticipationSection;
// ...existing code...
