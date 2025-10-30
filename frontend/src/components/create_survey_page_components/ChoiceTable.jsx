import ChoiceRow from "./ChoiceRow";
import { useTranslation } from "react-i18next";

const ChoiceTable = ({
  columns = [],
  rows = [],
  addRow,
  deleteRow,
  addColumn,
  removeColumn,
  updateCell,
  setSelectAllMandatory,
  selectAllMandatory
}) => {
  const { t } = useTranslation();

  const handleAddColumn = () => {
    const name = window.prompt(t("Anna sarakkeen nimi"));
    if (!name) return;
    addColumn(name.trim());
  };

  return (
    <div>
      <table className="table table-dark table-striped table-hover choice-table-main">
        <thead>
          <tr>
            <th>
              {t("Pakota minimikoko")}
              <label style={{ display: "flex", alignItems: "center" }}>
                <input
                  type="checkbox"
                  checked={!!selectAllMandatory}
                  onChange={(e) => setSelectAllMandatory?.(e.target.checked)}
                />
              </label>
            </th>

            <th>{t("Nimi")}</th>
            <th>{t("Enimmäispaikat")}</th>
            <th>{t("Ryhmän minimikoko")}</th>

            {columns.map(({ name }) => (
              <th key={name}>
                <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  <span>{name}</span>
                  <button type="button" onClick={() => removeColumn(name)}>
                    ✖
                  </button>
                </div>
              </th>
            ))}

            <th>
              <button type="button" onClick={handleAddColumn}>
                + {t("Lisää tietokenttä")}
              </button>
            </th>

            <th></th>
          </tr>
        </thead>

        <tbody>
          {rows.map((row) => (
            <ChoiceRow
              key={row.id}
              row={row}
              columns={columns}
              updateCell={updateCell}
              onDelete={() => deleteRow(row.id)}
            />
          ))}
        </tbody>
      </table>

      <div>
        <button
          className="new-row-input btn btn-secondary"
          type="button"
          onClick={addRow}
        >
          + {t("Lisää vaihtoehto")}
        </button>
      </div>
    </div>
  );
};

export default ChoiceTable;
