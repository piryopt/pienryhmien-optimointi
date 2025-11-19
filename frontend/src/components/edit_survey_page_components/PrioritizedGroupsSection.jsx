import { useTranslation } from "react-i18next";
import { useMemo } from "react";
import ChoicesDisplayTable from "./ChoicesDisplayTable";

const PrioritizedGroupsSection = ({ choices }) => {
  const { t } = useTranslation();

  const { columns, rows } = useMemo(() => {
    const colSet = new Set();
    const normalizedRows = (Array.isArray(choices) ? choices : []).map((c) => {
      const row = { ...c };
      if (Array.isArray(c.infos)) {
        c.infos.forEach((infoObj) => {
          const key = Object.keys(infoObj || {})[0];
          if (key) {
            colSet.add(key);
            row[key] = infoObj[key];
          }
        });
      }
      return row;
    });
    const columns = Array.from(colSet).map((name) => ({ name }));
    return { columns, rows: normalizedRows };
  }, [choices]);

  return (
    <div>
      <h2>{t("Priorisoitavat ryhmät")}</h2>
      <ChoicesDisplayTable columns={columns} rows={rows} />
    </div>
  );
};

export default PrioritizedGroupsSection;
