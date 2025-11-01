import { useTranslation } from "react-i18next";
import { useState, useRef } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useNotification } from "../context/NotificationContext";
import { buildCreateSurveySchema } from "../utils/validations/createSurveyValidations";
import Header from "../components/create_survey_page_components/Header";
import SurveyNameInput from "../components/create_survey_page_components/SurveyNameInput";
import StageNameInput from "../components/create_survey_page_components/StageNameInput";
import SurveyDateOfClosing from "../components/create_survey_page_components/SurveyDateOfClosing";
import SurveyDescription from "../components/create_survey_page_components/SurveyDescription";
import MinChoicesSection from "../components/create_survey_page_components/MinChoicesSection";
import DenyChoicesSection from "../components/create_survey_page_components/DenyChoicesSection";
import SearchVisibilitySection from "../components/create_survey_page_components/SearchVisibilitySection";
import PrioritizedGroupsDescription from "../components/create_survey_page_components/PrioritizedGroupsDescription";
import ChoiceTable from "../components/create_survey_page_components/ChoiceTable";
import "../static/css/createSurveyPage.css";
import Button from 'react-bootstrap/Button';

const SurveyMultiphaseCreate = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();

  const schema = buildCreateSurveySchema(t);

  // Manage multiple choice tables (stages)
  const stageNextId = useRef(1);
  const [newStageName, setNewStageName] = useState("");
  const [tables, setTables] = useState([
    {
      id: 1,
      name: "", // stage name
      nextRowId: 1,
      columns: [],
      rows: [{ id: 1, mandatory: false, name: "", max_spaces: "", min_size: "" }],
      selectAllMandatory: false
    }
  ]);

  const addStage = () => {
    const id = ++stageNextId.current;
    setTables((ts) => [
      ...ts,
      {
        id,
        name: newStageName || "",
        nextRowId: 1,
        columns: [],
        rows: [{ id: 1, mandatory: false, name: "", max_spaces: "", min_size: "" }],
        selectAllMandatory: false
      }
    ]);
    setNewStageName("");
  };

  const updateStageName = (tableId, name) =>
    setTables((ts) => ts.map((t) => (t.id !== tableId ? t : { ...t, name })));

  const addRow = (tableId) => {
    setTables((ts) =>
      ts.map((t) => {
        if (t.id !== tableId) return t;
        const id = t.nextRowId + 1;
        const extra = t.columns.reduce((a, c) => ({ ...a, [c.name]: "" }), {});
        return {
          ...t,
          nextRowId: id,
          rows: [...t.rows, { id, mandatory: false, name: "", max_spaces: "", min_size: "", ...extra }]
        };
      })
    );
  };

  const deleteRow = (tableId, id) =>
    setTables((ts) =>
      ts.map((t) => (t.id !== tableId ? t : { ...t, rows: t.rows.filter((r) => r.id !== id) }))
    );

  const updateCell = (tableId, id, key, value) =>
    setTables((ts) =>
      ts.map((t) =>
        t.id !== tableId
          ? t
          : { ...t, rows: t.rows.map((row) => (row.id === id ? { ...row, [key]: value } : row)) }
      )
    );

  const addColumn = (tableId, name) => {
    if (!name) return;
    setTables((ts) =>
      ts.map((t) => {
        if (t.id !== tableId) return t;
        if (t.columns.find((c) => c.name === name)) return t;
        return {
          ...t,
          columns: [...t.columns, { name, validationRegex: "", validationText: "" }],
          rows: t.rows.map((r) => ({ ...r, [name]: "" }))
        };
      })
    );
  };

  const removeColumn = (tableId, name) =>
    setTables((ts) =>
      ts.map((t) => {
        if (t.id !== tableId) return t;
        return {
          ...t,
          columns: t.columns.filter((c) => c.name !== name),
          rows: t.rows.map((r) => {
            const copy = { ...r };
            delete copy[name];
            return copy;
          })
        };
      })
    );

  const setTableSelectAllMandatory = (tableId, value) =>
    setTables((ts) =>
      ts.map((t) =>
        t.id !== tableId ? t : { ...t, selectAllMandatory: value, rows: t.rows.map((r) => ({ ...r, mandatory: value })) }
      )
    );

  const setChoices = () => {
    // Combine choices from all tables; include stageId and stageName
    const choicesEntry = tables.flatMap((t) =>
      t.rows.map((r) => {
        const base = {
          stageId: t.id,
          stageName: t.name ?? "",
          mandatory: !!r.mandatory,
          name: r.name,
          max_spaces: Number(r.max_spaces) || 0,
          min_size: Number(r.min_size) || 0
        };
        t.columns.forEach((c) => (base[c.name] = r[c.name] ?? ""));
        return base;
      })
    );
    return choicesEntry;
  };

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      groupname: "",
      enddate: null,
      endtime: "00:00",
      choices: [],
      minchoices: 1,
      surveyInformation: "",
      minChoicesSetting: "all",
      denyChoicesSetting: "hide",
      allowedDeniedChoices: "",
      allowSearchVisibility: false
    },
    mode: "onBlur"
  });

  const { handleSubmit } = methods;

  const onSubmit = async (data) => {
    const choices = setChoices();
    const payload = { ...data, choices };
    console.log("Submitting survey with payload:", payload);
  };

  return (
    <div>
      <Header />
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <SurveyNameInput />
          <SurveyDateOfClosing />
          <SurveyDescription />
          <MinChoicesSection />
          <DenyChoicesSection />
          <SearchVisibilitySection />
          <PrioritizedGroupsDescription />

          {tables.map((table) => (
            <div key={table.id} style={{ marginBottom: "65px" }}>
              <div className="d-flex align-items-left mb-4">
                <div className="column" style={{ marginRight: '10px' }}>
                  <StageNameInput
                    value={table.name}
                    onChange={(val) => updateStageName(table.id, val)}
                    placeholder={t("Vaiheen tunniste")}
                  />
                </div>
                <div className="column">
                <Button variant="danger" onClick={() => setTables((ts) => ts.filter((t) => t.id !== table.id))}>
                    {t("Poista vaihe")}
                  </Button>
                </div>
              </div>
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
          ))}
          <div className="mb-4" style={{ marginTop: "40px" }}>
              <Button variant="primary" onClick={addStage}>
                + {t("Lisää vaihe")}
              </Button>
            </div>
          <button type="submit" className="btn btn-success">
            {t("Luo kysely")}
          </button>
        </form>
      </FormProvider>
    </div>
  );
};

export default SurveyMultiphaseCreate;