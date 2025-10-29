export const validateSurvey = (t, groupname, endDate, rows, columns) => {
  const errs = [];

  if (!groupname || groupname.trim().length < 5)
    errs.push(t("Kyselyn nimen tulee olla vähintään 5 merkkiä pitkä"));

  if (!/^\d{2}\.\d{2}\.\d{4}$/.test(endDate))
    errs.push(t("Päivämäärä pitää olla muodossa pp.kk.yyyy"));

  rows.forEach((r, i) => {
    if (!r.name?.trim())
      errs.push(t("Rivi {{n}}: nimi puuttuu", { n: i + 1 }));

    columns.forEach((col) => {
      if (!col.validationRegex || !r[col.name]) return;
      try {
        const re = new RegExp(col.validationRegex);
        if (!re.test(r[col.name])) {
          errs.push(`${t("Sarakkeen")} ${col.name}: ${col.validationText || t("Virheellinen arvo")}`);
        }
      } catch {
      }
    });
  });

  return errs;
};
