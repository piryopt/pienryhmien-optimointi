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
    minchoices: yup
      .number()
      .transform((val, orig) =>
        orig === "" || Number.isNaN(val) ? undefined : val
      )
      .when(["minChoicesSetting", "choices"], (values, schema) => {
        const [minChoicesSetting, choices = []] = values || [];

        // only validate when user explicitly chose "custom"
        if (minChoicesSetting !== "custom") {
          return schema.notRequired();
        }

        // defer validation until there are choices present
        if (!Array.isArray(choices) || choices.length === 0) {
          return schema.notRequired();
        }

        const max = Math.max(0, choices.length - 1);
        return schema
          .typeError(t("Kentän tulee olla kokonaisluku"))
          .integer(t("Kentän tulee olla kokonaisluku"))
          .required(t("Priorisoitujen ryhmien vähimmäismäärä vaaditaan"))
          .min(
            1,
            t("Priorisoitavien ryhmien vähimmäismäärän on oltava vähintään 1")
          )
          .max(
            max,
            t(
              "Priorisoitavien ryhmien vähimmäismäärän on oltava enintään {{max}}",
              { max }
            )
          );
      }),
    allowedDeniedChoices: yup
      .number()
      .transform((val, orig) =>
        orig === "" || Number.isNaN(val) ? undefined : val
      )
      .when(["denyChoicesSetting", "choices"], (values, schema) => {
        const [denyChoicesSetting, choices = []] = values || [];

        // only validate when user chose "show"
        if (denyChoicesSetting !== "show") {
          return schema.notRequired();
        }

        // ignore validation until there are choices present
        if (!Array.isArray(choices) || choices.length === 0) {
          return schema.notRequired();
        }

        const max = Math.max(0, choices.length - 1);
        return schema
          .typeError(
            t("Sallittujen kiellettyjen ryhmien määrän tulee olla kokonaisluku")
          )
          .integer(
            t("Sallittujen kiellettyjen ryhmien määrän tulee olla kokonaisluku")
          )
          .required(t("Sallittujen kiellettyjen ryhmien määrä vaaditaan"))
          .min(
            1,
            t("Sallittujen kiellettyjen ryhmien määrän on oltava vähintään 1")
          )
          .max(
            max,
            t(
              "Sallittujen kiellettyjen ryhmien määrän on oltava enintään {{max}}",
              { max }
            )
          );
      }),
    choices: yup.array().of(
      yup.object({
        name: yup
          .string()
          .required(t("Nimi vaaditaan"))
          .min(5, t("Nimi on liian lyhyt, oltava vähintään 5 merkkiä")),
        max_spaces: yup
          .number()
          .typeError(t("Kentän tulee olla kokonaisluku"))
          .integer(t("Kentän tulee olla kokonaisluku"))
          .min(1, t("Enimmäispaikkojen määrä on oltava vähintään 1"))
          .required(t("Enimmäispaikat vaaditaan")),
        min_size: yup
          .number()
          .typeError(t("Kentän tulee olla kokonaisluku"))
          .integer(t("Kentän tulee olla kokonaisluku"))
          .when("mandatory", {
            is: true,
            then: (schema) =>
              schema.min(1, t("Ryhmän minimikoon on oltava vähintään 1")),
            otherwise: (schema) =>
              schema.min(0, t("Minimikoon on oltava vähintään 0"))
          })
          .required(t("Ryhmän minimikoko vaaditaan"))
      })
    )
  });
};
