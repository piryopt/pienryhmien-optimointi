// ...existing code...
import { useEffect } from "react";
import { useFormContext } from "react-hook-form";
import { useTranslation } from "react-i18next";

const LimitParticipationSection = ({ setLimitParticipationVisible }) => {
  const { register, watch } = useFormContext();
  const { t } = useTranslation();

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
          {...register("limitParticipation")}
          value="true"
          onChange={() => setLimitParticipationVisible(true)}
        />
        <label htmlFor="limit-participation-yes">{t("Kyllä")}</label>

        <input
          type="radio"
          id="limit-participation-no"
          {...register("limitParticipation")}
          value="false"
          defaultChecked
          onChange={() => setLimitParticipationVisible(false)}
        />
        <label htmlFor="limit-participation-no">{t("Ei")}</label>
      </div>
    </section>
  );
};

export default LimitParticipationSection;
// ...existing code...