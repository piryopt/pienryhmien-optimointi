import { useState } from "react";
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
  choiceErrors = [],
  limitParticipationVisible = false
}) => {
  const { t } = useTranslation("create");

  const [isAddingColumn, setIsAddingColumn] = useState(false);
  const [newColumnName, setNewColumnName] = useState("");

  const handleAddColumnSubmit = () => {
    if (newColumnName.trim() !== "") {
      addColumn(newColumnName.trim());
      setNewColumnName("");
      setIsAddingColumn(false);
    }
  };

  const handleCancelAddColumn = () => {
    setNewColumnName("");
    setIsAddingColumn(false);
  };

  return (
    <div className="choice-table-wrapper">
      <table className="table table-dark table-striped table-hover choice-table-main">
        <thead>
          <tr id="column-delete-btns">
            {limitParticipationVisible ? (
              <td colSpan="5"></td>
            ) : (
              <td colSpan="4"></td>
            )}
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

            {limitParticipationVisible && (
              <th
                className="constant-header"
                col-validation-regex="\d+"
                validation-text={t("kokonaislukuja")}
              >
                {t("Osallistumiskerrat*")}
              </th>
            )}

            {columns.map(({ name }) => (
              <th key={name} className="variable-header">
                {name}
              </th>
            ))}

            <th className="variable-header" id="add-column-header">
              {isAddingColumn ? (
                <div className="d-flex align-items-center gap-2">
                  <input
                    type="text"
                    autoFocus
                    value={newColumnName}
                    className="form-control form-control-sm bg-dark text-light"
                    onChange={(e) => setNewColumnName(e.target.value)}
                    onBlur={handleCancelAddColumn}
                    onKeyDown={(e) => {
                      if (e.key === "Enter") handleAddColumnSubmit();
                      if (e.key === "Escape") handleCancelAddColumn();
                    }}
                  />
                </div>
              ) : (
                <button
                  type="button"
                  className="btn btn-sm btn-outline-light"
                  onClick={() => setIsAddingColumn(true)}
                >
                  + {t("Lisää tietokenttä")}
                </button>
              )}
            </th>
          </tr>
        </thead>

        <tbody id="choiceTable">
          {rows.map((row, idx) => (
            <ChoiceRow
              key={row.id}
              row={row}
              columns={columns}
              updateCell={updateCell}
              onDelete={() => deleteRow(row.id)}
              limitParticipationVisible={limitParticipationVisible}
              errors={choiceErrors?.[idx] ?? {}}
            />
          ))}
        </tbody>
      </table>

      <div>
        <button
          className="new-row-input btn btn-secondary"
          type="button"
          data-testid="add-choice-button"
          onClick={addRow}
        >
          + {t("Lisää vaihtoehto")}
        </button>
      </div>
    </div>
  );
};

export default ChoiceTable;
