import { useTranslation } from "react-i18next";
import { useMemo } from "react";
import ChoicesDisplayTable from "./ChoicesDisplayTable";

const PrioritizedGroupsSection = ({
  choices_not_shuffled,
  choices,
  multistage
}) => {
  const { t } = useTranslation();

  const singleStageTable = useMemo(() => {
    const rowsSource =
      !multistage && Array.isArray(choices_not_shuffled)
        ? choices_not_shuffled
        : Array.isArray(choices)
          ? choices
          : [];
    const infoKeySet = new Set();
    const normalizedRows = rowsSource.map((c) => {
      const row = { ...c };

      if (Array.isArray(c.infos)) {
        c.infos.forEach((infoObj) => {
          const key = Object.keys(infoObj || {})[0];
          if (key) {
            infoKeySet.add(key);
            row[key] = infoObj[key];
          }
        });
      }
      return row;
    });

    const columns = [];
    Array.from(infoKeySet).forEach((name) => columns.push({ name }));

    return { columns, rows: normalizedRows };
  }, [choices]);

  // when multistage, build an array of tables (one per stage)
  const stageTables = useMemo(() => {
    if (!multistage || !Array.isArray(choices)) return [];
    return choices.map((stage) => {
      const rowsSource = Array.isArray(stage.choices) ? stage.choices : [];
      const infoKeySet = new Set();
      const normalizedRows = rowsSource.map((c) => {
        const row = { ...c };

        if (Array.isArray(c.infos)) {
          c.infos.forEach((infoObj) => {
            const key = Object.keys(infoObj || {})[0];
            if (key) {
              infoKeySet.add(key);
              row[key] = infoObj[key];
            }
          });
        }
        return row;
      });
      const columns = [];
      Array.from(infoKeySet).forEach((name) => columns.push({ name }));
      return { name: stage.name, columns, rows: normalizedRows };
    });
  }, [choices, multistage]);

  return (
    <div>
      <h2>{t("Priorisoitavat ryhmät")}</h2>
      {!multistage && (
        <ChoicesDisplayTable
          columns={singleStageTable.columns}
          rows={singleStageTable.rows}
          limitParticipationVisible={
            Array.isArray(singleStageTable.rows) &&
            singleStageTable.rows.length > 0 &&
            singleStageTable.rows.some((r) => Number(r.participation_limit) > 0)
          }
        />
      )}

      {multistage &&
        stageTables.map((stage) => (
          <div key={stage.name}>
            <h3>{stage.name}</h3>
            <ChoicesDisplayTable
              columns={stage.columns}
              rows={stage.rows}
              limitParticipationVisible={
                Array.isArray(stage.rows) &&
                stage.rows.length > 0 &&
                stage.rows.some((r) => Number(r.participation_limit) > 0)
              }
            />
          </div>
        ))}
    </div>
  );
};

export default PrioritizedGroupsSection;
