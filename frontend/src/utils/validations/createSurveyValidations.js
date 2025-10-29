import * as yup from "yup";
import { parse, format } from "date-fns";

export const buildCreateSurveySchema = (t) => {
  return yup.object({
    groupname: yup
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
    minChoicesSetting: yup.string().oneOf(["all", "custom"]).required(),
    minchoices: yup
      .number()
      .typeError(t("Kentän tulee olla kokonaisluku"))
      .integer(t("Kentän tulee olla kokonaisluku"))
      .min(0, t("Kentän tulee olla vähintään 0"))
      .when("minChoicesSetting", {
        is: "custom",
        then: (schema) =>
          schema.required(t("Priorisoitujen ryhmien vähimmäismäärä vaaditaan")),
        otherwise: (schema) => schema.notRequired().default(1)
      })
  });
};
