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
  selectAllMandatory,
}) => {
  const { t } = useTranslation();

  const handleAddColumn = () => {
    const name = window.prompt(t("Anna sarakkeen nimi"));
    if (!name) return;
    addColumn(name.trim());
  };

  return (
    <div className="choice-table-wrapper">
      <table className="table table-dark table-striped table-hover choice-table-main">
        <thead>
          <tr id="column-delete-btns">
            <td colSpan="4"></td>
            {columns.map(({ name }) => (
              <th key={name} className="variable-header">
                <div
                  className="delete-col-btn-visible"
                  onClick={() => removeColumn(name)}
                  title={t("Poista sarake")}
                ></div>
                <span>{name}</span>
              </th>

            ))}
            <td></td>
          </tr>

          <tr id="choice-table-headers">
            <th>
              <label>{t("Pakota minimikoko")}</label>
              <input
                type="checkbox"
                id="select-all-choices"
                checked={!!selectAllMandatory}
                onChange={(e) => setSelectAllMandatory?.(e.target.checked)}
              />
            </th>

            <th
              className="constant-header"
              col-validation-regex=".{5,}"
              validation-text={t("yli 5 merkkiä pitkiä")}
            >
              {t("Nimi")}
            </th>

            <th
              className="constant-header"
              col-validation-regex="\d+"
              validation-text={t("kokonaislukuja")}
            >
              {t("Enimmäispaikat")}
            </th>

            <th
              className="constant-header"
              col-validation-regex="\d+"
              validation-text={t("kokonaislukuja")}
            >
              {t("Ryhmän minimikoko")}
            </th>

            {columns.map(({ name }) => (
              <th key={name} className="variable-header">
                {name}
              </th>
            ))}

            <th className="variable-header" id="add-column-header">
              <button
                type="button"
                className="btn btn-sm btn-outline-light"
                onClick={handleAddColumn}
              >
                + {t("Lisää tietokenttä")}
              </button>
            </th>
          </tr>
        </thead>

        <tbody id="choiceTable">
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
