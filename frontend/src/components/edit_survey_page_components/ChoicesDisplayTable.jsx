import { useTranslation } from "react-i18next";
import ChoiceRowDisplay from "./ChoiceRowDisplay";

const ChoicesDisplayTable = ({
  columns = [],
  rows = [],
  limitParticipationVisible = false
}) => {
  const { t } = useTranslation("create");

  return (
    <div className="choice-table-wrapper">
      <table className="table table-dark table-striped table-hover choice-table-main">
        <thead>
          <tr id="choice-table-headers">
            <th>
              <label>{t("Pakota minimikoko")}</label>
            </th>

            <th className="constant-header">{t("Nimi")}</th>

            <th className="constant-header">{t("Enimmäispaikat")}</th>

            <th className="constant-header">{t("Ryhmän minimikoko")}</th>

            {limitParticipationVisible && (
              <th className="constant-header">{t("Osallistumiskerrat*")}</th>
            )}

            {columns.map(({ name }) => (
              <th key={name} className="variable-header">
                {name}
              </th>
            ))}

            <th className="variable-header" id="add-column-header">
              {/* placeholder to match original layout */}
            </th>
          </tr>
        </thead>

        <tbody id="choiceTable">
          {rows.map((row) => (
            <ChoiceRowDisplay
              key={row.id}
              row={row}
              columns={columns}
              limitParticipationVisible={limitParticipationVisible}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ChoicesDisplayTable;
