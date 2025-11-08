import * as yup from "yup";

export const buildEditSurveySchema = (t) => {
  return yup.object({
    surveyName: yup
      .string()
      .required(t("Kyselyn nimen tulee olla vähintään 5 merkkiä pitkä"))
      .min(5, t("Kyselyn nimen tulee olla vähintään 5 merkkiä pitkä")),
    enddate: yup
      .date()
      .required(t("Valitse päättymispäivä"))
      .typeError(t("Päivämäärä on virheellinen")),
    endtime: yup
      .string()
      .required(t("Valitse päättymisaika"))
      .test(
        "end-in-future",
        t("Vastausajan päättyminen ei voi olla menneisyydessä"),
        function (value) {
          const { enddate } = this.parent;
          if (!enddate || !value) return true;
          const [hh, mm] = String(value).split(":").map(Number);
          const combined = new Date(enddate);
          combined.setHours(hh || 0, mm || 0, 0, 0);
          return combined.getTime() > Date.now();
        }
      ),
  });
};


export const buildEditSurveyAdminSchema = (t) => {
  return yup.object({
    adminEmail: yup
      .string()
      .required(t("Anna sähköpostiosoite"))
      .email(t("Antamasi sähköpostiosoite ei ole kelvollinen"))
  })
}