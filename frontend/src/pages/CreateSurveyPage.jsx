import { useState, useEffect, useRef, useCallback } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useTranslation } from "react-i18next";
import { useNotification } from "../context/NotificationContext";
import { buildCreateSurveySchema } from "../utils/validations/createSurveyValidations";
import { format } from "date-fns";
import csrfService from "../services/csrf";
import Header from "../components/create_survey_page_components/Header";
import SurveyNameInput from "../components/create_survey_page_components/SurveyNameInput";
import SurveyDateOfClosing from "../components/create_survey_page_components/SurveyDateOfClosing";
import SurveyDescription from "../components/create_survey_page_components/SurveyDescription";
import MinChoicesSection from "../components/create_survey_page_components/MinChoicesSection";
import DenyChoicesSection from "../components/create_survey_page_components/DenyChoicesSection";
import SearchVisibilitySection from "../components/create_survey_page_components/SearchVisibilitySection";
import PrioritizedGroupsDescription from "../components/create_survey_page_components/PrioritizedGroupsDescription";
import ChoiceTable from "../components/create_survey_page_components/ChoiceTable";
import { parseCsvFile, updateTableFromCSV } from "../services/csv";
import "../static/css/createSurveyPage.css";

const CreateSurveyPage = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();

  const schema = buildCreateSurveySchema(t);

  const nextRowId = useRef(1);
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([
    { id: 1, mandatory: false, name: "", max_spaces: "", min_size: "" }
  ]);
  const [selectAllMandatory, setSelectAllMandatory] = useState(false);

  useEffect(() => {
    setRows((r) => r.map((x) => ({ ...x, mandatory: selectAllMandatory })));
  }, [selectAllMandatory]);

  const addRow = () => {
    const id = ++nextRowId.current;
    const extra = columns.reduce((a, c) => ({ ...a, [c.name]: "" }), {});
    setRows((r) => [
      ...r,
      { id, mandatory: false, name: "", max_spaces: "", min_size: "", ...extra }
    ]);
  };

  const deleteRow = (id) => setRows((r) => r.filter((x) => x.id !== id));
  const updateCell = (id, key, value) =>
    setRows((r) =>
      r.map((row) => (row.id === id ? { ...row, [key]: value } : row))
    );

  const addColumn = (name) => {
    if (!name || columns.find((c) => c.name === name)) return;
    setColumns((c) => [
      ...c,
      { name, validationRegex: "", validationText: "" }
    ]);
    setRows((rs) => rs.map((r) => ({ ...r, [name]: "" })));
  };

  const removeColumn = (name) => {
    setColumns((c) => c.filter((x) => x.name !== name));
    setRows((rs) =>
      rs.map((r) => {
        const copy = { ...r };
        delete copy[name];
        return copy;
      })
    );
  };

  const setChoices = () => {
    const choicesEntry = rows.map((r) => {
      const base = {
        mandatory: !!r.mandatory,
        name: r.name,
        max_spaces: Number(r.max_spaces) || 0,
        min_size: Number(r.min_size) || 0
      };
      columns.forEach((c) => (base[c.name] = r[c.name] ?? ""));
      return base;
    });
    return choicesEntry;
  };

  const importCsv = useCallback(
    async (file) => {
      try {
        const parsed = await parseCsvFile(file); // returns array-of-arrays
        if (!parsed || parsed.length < 2) return;
        const headers = parsed[0].map((h) => (h ?? "").toString().trim());
        const dataRows = parsed.slice(1);
        const existingTable = { columns, rows, nextRowId: nextRowId.current };
        const merged = updateTableFromCSV(headers, dataRows, existingTable);
        setColumns(merged.columns);
        setRows(merged.rows);
        nextRowId.current = merged.nextRowId;
      } catch (err) {
        // handle error (toast/log)
        console.error("CSV import failed", err);
      }
    },
    [columns, rows]
  );

  const methods = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      groupname: "",
      enddate: null,
      endtime: "00:00",
      choices: [],
      minchoices: 1,
      surveyInformation: "",
      // radio setting defaults
      minChoicesSetting: "all",
      denyChoicesSetting: "hide",
      allowedDeniedChoices: 0,
      allowSearchVisibility: false
    },
    mode: "onBlur"
  });

  const { handleSubmit } = methods;

  const onSubmit = async (data) => {
    const csrfToken = await csrfService.fetchCsrfToken();
    const payload = {
      surveyGroupname: data.groupname,
      surveyInformation: data.surveyInformation || "",
      choices: setChoices() || [],
      minchoices: data.minchoices ?? 1,
      enddate: data.enddate ? format(data.enddate, "dd.MM.yyyy") : "",
      endtime: data.endtime || "",
      allowedDeniedChoices: data.allowedDeniedChoices || 0,
      allowSearchVisibility: data.allowSearchVisibility || false
    };

    const extractMessage = (json, res) => {
      if (!json) return res?.statusText || t("Kyselyn luonti epäonnistui");
      if (typeof json === "string") return json;
      return (
        json.msg ||
        json.message ||
        res?.statusText ||
        t("Kyselyn luonti epäonnistui")
      );
    };

    try {
      console.log(payload.choices);
      const res = await fetch("http://localhost:5001/surveys/create", {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(payload)
      });

      let json = null;
      try {
        json = await res.json();
      } catch {
        json = null;
      }

      if (!res.ok) {
        const msg = extractMessage(json, res);
        showNotification(msg, "error");
        return;
      }

      if (!json || String(json.status) !== "1") {
        const msg = extractMessage(json, res);
        showNotification(msg, "error");
        return;
      }

      showNotification(json.msg || t("Kysely luotu onnistuneesti"), "success");
    } catch (err) {
      showNotification(
        err?.message || t("Kyselyn luonti epäonnistui"),
        "error"
      );
    }
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
          <PrioritizedGroupsDescription importCsv={importCsv} />
          <ChoiceTable
            columns={columns}
            rows={rows}
            addRow={addRow}
            deleteRow={deleteRow}
            addColumn={addColumn}
            removeColumn={removeColumn}
            updateCell={updateCell}
            setSelectAllMandatory={setSelectAllMandatory}
            selectAllMandatory={selectAllMandatory}
          />
          <br />
          <button type="submit" className="btn btn-primary">
            {t("Luo kysely")}
          </button>
        </form>
      </FormProvider>
    </div>
  );
};

export default CreateSurveyPage;
