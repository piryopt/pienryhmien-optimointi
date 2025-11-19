import { useTranslation } from "react-i18next";
import Button from "react-bootstrap/Button";
import ChoiceTable from "../create_survey_page_components/ChoiceTable";
import StageNameInput from "../create_survey_page_components/StageNameInput";
import { imagesBaseUrl } from "../../utils/constants";
import "../../static/css/createSurveyPage.css";

const StageTables = ({
  tables,
  updateStageName,
  setTables,
  addRow,
  deleteRow,
  addColumn,
  removeColumn,
  updateCell,
  setTableSelectAllMandatory,
  importCsv,
  limitParticipationVisible,
  copyStage
}) => {
  const { t } = useTranslation();

  return (
    <>
      {tables.map((table) => (
        <div key={table.id} className="stage">
          <div className="d-flex align-items-start stage-name-delete">
            <div className="column stage-name-input">
              <StageNameInput
                value={table.name}
                onChange={(val) => updateStageName(table.id, val)}
                placeholder={t("Vaiheen tunniste")}
              />
            </div>
            <div className="column stage-delete-button">
              <Button
                variant="danger"
                onClick={() =>
                  setTables((ts) => ts.filter((t) => t.id !== table.id))
                }
              >
                {t("Poista vaihe")}
              </Button>
            </div>
            <div className="column stage-copy-button">
              <Button variant="primary" onClick={() => copyStage(table.id)}>
                <img
                  className="copy-icon"
                  src={`${imagesBaseUrl}/content_copy_white_36dp.svg`}
                />
                {t("Kopioi vaihe")}
              </Button>
            </div>
            <div className="column">
              <input
                id={`choiceFileInput-${table.id}`}
                type="file"
                accept=".csv,text/csv"
                style={{ display: "none" }}
                onChange={(e) => {
                  const f = e.target.files && e.target.files[0];
                  if (f && importCsv) importCsv(table.id, f);
                  // reset so the same file can be re-selected later
                  e.target.value = "";
                }}
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
              updateCell={(rowId, key, value) =>
                updateCell(table.id, rowId, key, value)
              }
              setSelectAllMandatory={(val) =>
                setTableSelectAllMandatory(table.id, val)
              }
              selectAllMandatory={table.selectAllMandatory}
              choiceErrors={table.choiceErrors || []}
              limitParticipationVisible={limitParticipationVisible}
            />
          </div>
        </div>
      ))}
    </>
  );
};

export default StageTables;
