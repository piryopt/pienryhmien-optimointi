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
import { useSearchParams } from "react-router-dom";
import surveyService from "../services/surveys";
import "../static/css/createSurveyPage.css";
import { baseUrl } from "../utils/constants";

const CreateSurveyPage = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const [searchParams] = useSearchParams();

  const schema = buildCreateSurveySchema(t);
  const [choiceErrors, setChoiceErrors] = useState([]);
  const nextRowId = useRef(1);
  const [columns, setColumns] = useState([]);
  const [rows, setRows] = useState([
    { id: 1, mandatory: false, name: "", max_spaces: "", min_size: "" }
  ]);
  const [selectAllMandatory, setSelectAllMandatory] = useState(false);

  const templateId = searchParams.get("fromtemplate");

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

  useEffect(() => {
    if (!templateId) return;

    const loadTemplate = async () => {
      try {
        const data = await surveyService.getSurvey(templateId);

        if (!data.survey || !Array.isArray(data.choices)) return;

        methods.setValue("groupname", data.survey.name || "");
        methods.setValue("surveyInformation", data.survey.description || "");

        const dynamicCols = new Set();
        data.choices.forEach((choice) => {
          choice.infos?.forEach((infoObj) => {
            Object.keys(infoObj).forEach((key) => dynamicCols.add(key));
          });
        });
        dynamicCols.forEach((colName) => addColumn(colName));

        const choices = data.choices.map((c, i) => {
          const row = {
            id: i + 1,
            mandatory: !!c.mandatory,
            name: c.name || "",
            max_spaces: c.slots || 0,
            min_size: c.min_size || 0
          };

          c.infos?.forEach((infoObj) => {
            Object.entries(infoObj).forEach(([key, value]) => {
              row[key] = value;
            });
          });
          return row;
        });

        nextRowId.current = choices.length;
        setRows(choices);
      } catch (error) {
        console.error("Failed to load survey template:", error);
      }
    };

    loadTemplate();
  }, [templateId]);

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
  const updateCell = (id, key, value) => {
    setRows((r) => {
      const newRows = r.map((row) =>
        row.id === id ? { ...row, [key]: value } : row
      );

      setChoiceErrors((prev = []) => {
        const copy = [...prev];
        const idx = newRows.findIndex((row) => row.id === id);
        if (idx >= 0) {
          const rowErr = copy[idx] ? { ...copy[idx] } : {};
          if (rowErr && Object.prototype.hasOwnProperty.call(rowErr, key)) {
            delete rowErr[key];
            copy[idx] = rowErr;
          }
        }
        return copy;
      });

      return newRows;
    });
  };

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
      const parseNumberOrUndefined = (val) =>
        val === "" || val === null || typeof val === "undefined"
          ? undefined
          : Number(val);

      const base = {
        mandatory: !!r.mandatory,
        name: r.name,
        max_spaces: parseNumberOrUndefined(r.max_spaces),
        min_size: parseNumberOrUndefined(r.min_size)
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
        console.error("CSV import failed", err);
      }
    },
    [columns, rows]
  );

  const onSubmit = async (data) => {
    try {
      await schema.validate(
        { ...data, choices: setChoices() },
        { abortEarly: false }
      );
      setChoiceErrors([]);
    } catch (validationError) {
      const perRowErrors = rows.map(() => ({}));
      if (
        validationError &&
        validationError.inner &&
        validationError.inner.length
      ) {
        validationError.inner.forEach((err) => {
          if (!err.path) return;
          const m = err.path.match(/^choices\[(\d+)\]\.(.+)$/);
          if (m) {
            const idx = Number(m[1]);
            const field = m[2];
            perRowErrors[idx] = perRowErrors[idx] || {};
            perRowErrors[idx][field] = perRowErrors[idx][field] || err.message;
          }
        });
      }
      setChoiceErrors(perRowErrors);
      return;
    }

    const csrfToken = await csrfService.fetchCsrfToken();
    const payload = {
      surveyGroupname: data.groupname,
      surveyInformation: data.surveyInformation || "",
      choices: setChoices() || [],
      minchoices: data.minchoices ?? 1,
      enddate: data.enddate ? format(data.enddate, "dd.MM.yyyy") : "",
      endtime: data.endtime || "",
      allowedDeniedChoices: data.allowedDeniedChoices || 0,
      allowSearchVisibility: data.searchVisibility || false
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
      const res = await fetch(`${baseUrl}/surveys/create`, {
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
            choiceErrors={choiceErrors}
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
