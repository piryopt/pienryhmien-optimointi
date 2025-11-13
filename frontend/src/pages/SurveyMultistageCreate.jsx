import { useTranslation } from "react-i18next";
import { useState, useRef } from "react";
import { useForm, FormProvider } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import { useNotification } from "../context/NotificationContext";
import { buildCreateSurveySchema } from "../utils/validations/createSurveyValidations";
import MultistageSurveyHeader from "../components/create_multistage_survey_components/MultistageSurveyHeader";
import SurveyNameInput from "../components/create_survey_page_components/SurveyNameInput";
import SurveyDateOfClosing from "../components/create_survey_page_components/SurveyDateOfClosing";
import SurveyDescription from "../components/create_survey_page_components/SurveyDescription";
import MinChoicesSection from "../components/create_survey_page_components/MinChoicesSection";
import DenyChoicesSection from "../components/create_survey_page_components/DenyChoicesSection";
import AllowAbsencesSection from "../components/create_multistage_survey_components/AllowAbsences";
import LimitParticipationSection from "../components/create_multistage_survey_components/LimitParticipation";
import SearchVisibilitySection from "../components/create_survey_page_components/SearchVisibilitySection";
import MultistageSurveyPrioritizedGroupsDescription from "../components/create_multistage_survey_components/MultistageSurveyPrioritizedGroupsDescription";
import StageTables from "../components/create_multistage_survey_components/StageTables";
import Button from "react-bootstrap/Button";
import { format } from "date-fns";
import csrfService from "../services/csrf";
import "../static/css/createSurveyPage.css";
import { parseCsvFile, updateTableFromCSV } from "../services/csv";

const SurveyMultistageCreate = () => {
  const { t } = useTranslation();
  const { showNotification } = useNotification();
  const [limitParticipationVisible, setLimitParticipationVisible] =
    useState(false);

  const schema = buildCreateSurveySchema(t);

  const stageNextId = useRef(1);
  const [newStageName, setNewStageName] = useState("");
  const [tables, setTables] = useState([]);

  const addStage = () => {
    const id = stageNextId.current++;
    setTables((ts) => [
      ...ts,
      {
        id,
        name: newStageName || "",
        nextRowId: 1,
        columns: [],
        rows: [
          { id: 1, mandatory: false, name: "", max_spaces: "", min_size: "" }
        ],
        selectAllMandatory: false,
        choiceErrors: []
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
          rows: [
            ...t.rows,
            {
              id,
              mandatory: false,
              name: "",
              max_spaces: "",
              min_size: "",
              ...extra
            }
          ]
        };
      })
    );
  };

  const deleteRow = (tableId, id) =>
    setTables((ts) =>
      ts.map((t) =>
        t.id !== tableId ? t : { ...t, rows: t.rows.filter((r) => r.id !== id) }
      )
    );

  const updateCell = (tableId, id, key, value) =>
    setTables((ts) =>
      ts.map((t) => {
        if (t.id !== tableId) return t;

        const newRows = t.rows.map((row) =>
          row.id === id ? { ...row, [key]: value } : row
        );

        const rowIndex = t.rows.findIndex((r) => r.id === id);
        const newChoiceErrors = Array.isArray(t.choiceErrors)
          ? t.choiceErrors.map((err) => ({ ...err }))
          : [];

        if (rowIndex >= 0 && newChoiceErrors[rowIndex]) {
          if (
            Object.prototype.hasOwnProperty.call(newChoiceErrors[rowIndex], key)
          ) {
            const copyRowErr = { ...newChoiceErrors[rowIndex] };
            delete copyRowErr[key];
            newChoiceErrors[rowIndex] = copyRowErr;
          }
        }

        return { ...t, rows: newRows, choiceErrors: newChoiceErrors };
      })
    );

  const addColumn = (tableId, name) => {
    if (!name) return;
    setTables((ts) =>
      ts.map((t) => {
        if (t.id !== tableId) return t;
        if (t.columns.find((c) => c.name === name)) return t;
        return {
          ...t,
          columns: [
            ...t.columns,
            { name, validationRegex: "", validationText: "" }
          ],
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
        t.id !== tableId
          ? t
          : {
              ...t,
              selectAllMandatory: value,
              rows: t.rows.map((r) => ({ ...r, mandatory: value }))
            }
      )
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
      minChoicesSetting: "all",
      denyChoicesSetting: "hide",
      allowedDeniedChoices: "",
      allowSearchVisibility: false
    },
    mode: "onBlur"
  });

  const importCsvToTable = async (tableId, file) => {
    if (!file) return;
    const parsed = await parseCsvFile(file);
    if (!parsed || parsed.length <= 1) return;

    const headers = parsed[0].map((h) => (h ?? "").toString().trim());
    const rowsToParse = parsed
      .slice(1)
      .filter((r) => r.some((c) => String(c || "").trim() !== ""));

    setTables((ts) =>
      ts.map((t) => {
        if (t.id !== tableId) return t;
        const update = updateTableFromCSV(headers, rowsToParse, t);
        return {
          ...t,
          columns: update.columns,
          rows: update.rows,
          nextRowId: update.nextRowId
        };
      })
    );
  };

  const { handleSubmit } = methods;

  const onSubmit = async (data) => {
    const csrfToken = await csrfService.fetchCsrfToken();

    const parseNumberOrUndefined = (val) =>
      val === "" || val === null || typeof val === "undefined"
        ? undefined
        : Number(val);

    console.log(
      "DEBUG: tables before payload:",
      JSON.stringify(tables, null, 2)
    );

    const stages = tables.map((t) => ({
      id: t.id,
      name: t.name || "",
      columns: t.columns.map((c) => ({ ...c })),
      choices: t.rows.map((r) => {
        const choice = {
          mandatory: !!r.mandatory,
          name: r.name || "",
          max_spaces: parseNumberOrUndefined(r.max_spaces),
          min_size: parseNumberOrUndefined(r.min_size),
          participation_limit: parseNumberOrUndefined(r.participation_limit)
        };
        t.columns.forEach((c) => {
          choice[c.name] = r[c.name] ?? "";
        });
        return choice;
      })
    }));
    let anyValidationFailed = false;
    await Promise.all(
      stages.map(async (stage) => {
        try {
          await schema.validate(
            {
              groupname: data.groupname,
              enddate: data.enddate,
              endtime: data.endtime,
              minchoices: data.minchoices,
              minChoicesSetting: data.minChoicesSetting,
              choices: stage.choices
            },
            { abortEarly: false }
          );
          // clear previous errors for this stage
          setTables((ts) =>
            ts.map((t) => (t.id !== stage.id ? t : { ...t, choiceErrors: [] }))
          );
        } catch (validationError) {
          anyValidationFailed = true;
          const perRowErrors = (stage.choices || []).map(() => ({}));
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
                perRowErrors[idx][field] =
                  perRowErrors[idx][field] || err.message;
              }
            });
          }
          setTables((ts) =>
            ts.map((t) =>
              t.id !== stage.id ? t : { ...t, choiceErrors: perRowErrors }
            )
          );
        }
      })
    );

    if (anyValidationFailed) {
      return;
    }

    console.log(
      "DEBUG: built stages payload:",
      JSON.stringify(stages, null, 2)
    );

    const allowedDenied = data.allowedDeniedChoices;
    console.log(data);

    const payload = {
      surveyGroupname: data.groupname,
      surveyInformation: data.surveyInformation || "",
      stages,
      minchoices: data.minchoices ?? 1,
      enddate: data.enddate ? format(data.enddate, "dd.MM.yyyy") : "",
      endtime: data.endtime || "",
      allowedDeniedChoices: allowedDenied,
      allowSearchVisibility: data.allowSearchVisibility || false,
      allowAbsences: data.allowAbsences || false
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
      const res = await fetch(
        "http://localhost:5001/api/multistage/survey/create",
        {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
          },
          body: JSON.stringify(payload)
        }
      );

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
      <MultistageSurveyHeader />
      <FormProvider {...methods}>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <SurveyNameInput />
          <SurveyDateOfClosing />
          <SurveyDescription />
          <MinChoicesSection />
          <DenyChoicesSection />
          <AllowAbsencesSection />
          <LimitParticipationSection
            limitParticipationVisible={limitParticipationVisible}
            setLimitParticipationVisible={setLimitParticipationVisible}
          />
          <SearchVisibilitySection />
          <MultistageSurveyPrioritizedGroupsDescription />
          <StageTables
            tables={tables}
            updateStageName={updateStageName}
            setTables={setTables}
            addRow={addRow}
            deleteRow={deleteRow}
            addColumn={addColumn}
            removeColumn={removeColumn}
            updateCell={updateCell}
            setTableSelectAllMandatory={setTableSelectAllMandatory}
            importCsv={importCsvToTable}
            limitParticipationVisible={limitParticipationVisible}
          />
          <div className="mb-4">
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

export default SurveyMultistageCreate;
