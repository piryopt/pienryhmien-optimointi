import { useTranslation } from "react-i18next";
import Button from "react-bootstrap/Button";
import ChoiceTable from "../create_survey_page_components/ChoiceTable";
import StageNameInput from "../create_survey_page_components/StageNameInput";

const StageTables = ({ tables, updateStageName, setTables, addRow, deleteRow, addColumn, removeColumn, updateCell, setTableSelectAllMandatory }) => {
  const { t } = useTranslation();
  
  return (
    <>
    {tables.map((table) => (
      <div key={table.id} className="stage">
          <div className="d-flex align-items-start stage-name-delete" >
          <div className="column stage-name-input" >
            <StageNameInput
              value={table.name}
              onChange={(val) => updateStageName(table.id, val)}
              placeholder={t("Vaiheen tunniste")}
            />
          </div>
          <div className="column stage-delete-button" >
          <Button variant="danger" onClick={() => setTables((ts) => ts.filter((t) => t.id !== table.id))}>
              {t("Poista vaihe")}
            </Button>
          </div>
          <div className="column">
            <input
              id={`choiceFileInput-${table.id}`}
              type="file"
              accept=".csv,text/csv"
              style={{ display: "none" }}
            />
            <label
              htmlFor={`choiceFileInput-${table.id}`}
              className="btn btn-secondary"
              role="button"
            >
              {t("Tuo valinnat CSV-tiedostosta")}
            </label>
          </div>
        </div>
        <div style={{ marginTop: "0px" }}>
        <ChoiceTable
          columns={table.columns}
          rows={table.rows}
          addRow={() => addRow(table.id)}
          deleteRow={(rowId) => deleteRow(table.id, rowId)}
          addColumn={(name) => addColumn(table.id, name)}
          removeColumn={(name) => removeColumn(table.id, name)}
          updateCell={(rowId, key, value) => updateCell(table.id, rowId, key, value)}
          setSelectAllMandatory={(val) => setTableSelectAllMandatory(table.id, val)}
          selectAllMandatory={table.selectAllMandatory}
        />
        </div>
      </div>
    ))}
  </>
  );
}

export default StageTables;