import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import * as XLSX from "xlsx";
import { useNotification } from "../context/NotificationContext";
import surveyService from "../services/surveys";
import StageDropdown from "../components/survey_answers_page_components/StageDropdown";
import SurveyResultsTable from "../components/survey_results_page_components/SurveyResultsTable";
import Happiness from "../components/survey_results_page_components/Happiness";

const MultistageSurveyResultsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [surveyResultsData, setSurveyResultsData] = useState(null);
  const [stages, setStages] = useState([]);
  const [currStage, setCurrStage] = useState(null);
  const [currResults, setCurrResults] = useState([]);
  const [loading, setLoading] = useState(true);

  const [droppedGroups, setDroppedGroups] = useState([]);
  const [happinessData, setHappinessData] = useState([]);
  const [resultsSaved, setResultsSaved] = useState(false);
  const [results, setResults] = useState([]);

  const { t } = useTranslation("result");
  const { showNotification } = useNotification();

  useEffect(() => {
    const getSurveyResults = async () => {
      try {
        const response = await surveyService.getSurveyResultsData(id);
        if (!response.stageResults || !Array.isArray(response.stageResults)) {
          navigate(`/surveys/multistage/${id}/answers`, { replace: true });
          setSurveyResultsData(response);
          setStages([]);
          setCurrStage(null);
          setCurrResults([]);
          return;
        }

        setSurveyResultsData(response);
        const surveyStages = response.stageResults.map(
          (stage) => stage["stage"] || null
        );
        setStages(surveyStages);
        setCurrStage(surveyStages[0] ?? null);
        setCurrResults(response.stageResults[0] ?? null);
      } catch (err) {
        console.error("Error loading survey results", err);
      } finally {
        setTimeout(() => {
          setLoading(false);
        }, 1);
      }
    };
    getSurveyResults();
  }, []);

  useEffect(() => {
    if (!surveyResultsData || !Array.isArray(surveyResultsData.stageResults))
      return;
    const active =
      surveyResultsData.stageResults.find((s) => s.stage === currStage) ||
      surveyResultsData.stageResults[0] ||
      null;
    setCurrResults(active);

    if (active) {
      setResults(active.results || []);
      setDroppedGroups(active.droppedGroups || []);
      setHappinessData(active.happinessData || []);
      setResultsSaved(Boolean(surveyResultsData.resultsSaved));
    } else {
      setResults([]);
      setDroppedGroups([]);
      setHappinessData([]);
      setResultsSaved(false);
    }
  }, [currStage, surveyResultsData]);

  const exportToExcel = async () => {
    if (
      !surveyResultsData ||
      !Array.isArray(surveyResultsData.stageResults) ||
      surveyResultsData.stageResults.length === 0
    ) {
      showNotification(t("Ei tuloksia vietäväksi"), "warning");
      return;
    }

    let multistageMeta = null;
    try {
      multistageMeta = await surveyService.getMultiStageSurvey(id);
    } catch (err) {
      console.warn("Could not load multistage metadata for infos lookup", err);
    }

    const wb = XLSX.utils.book_new();

    for (let idx = 0; idx < surveyResultsData.stageResults.length; idx += 1) {
      const stageObj = surveyResultsData.stageResults[idx];
      try {
        const resultsArr = Array.isArray(stageObj.results)
          ? stageObj.results
          : [];
        const rawName = stageObj.stage || `${t("Vaihe")}_${idx + 1}`;
        const sheetName = String(rawName).substring(0, 31);

        if (!resultsArr || resultsArr.length === 0) {
          const infoRow = { [t("Info")]: t("Ei tuloksia tälle vaiheelle") };
          const ws = XLSX.utils.json_to_sheet([infoRow]);
          XLSX.utils.book_append_sheet(wb, ws, sheetName);
          continue;
        }

        const rawInfos = stageObj.infos ?? [];
        const infoKeys = [];
        const infoDefaults = {};
        const pushKey = (k, defaultVal) => {
          if (!k) return;
          const sk = String(k);
          if (!infoKeys.includes(sk)) infoKeys.push(sk);
          if (
            defaultVal !== undefined &&
            defaultVal !== null &&
            infoDefaults[sk] === undefined
          ) {
            infoDefaults[sk] = defaultVal;
          }
        };

        if (Array.isArray(rawInfos)) {
          rawInfos.forEach((entry) => {
            if (!entry) return;
            if (typeof entry === "string") {
              pushKey(entry, "");
            } else if (Array.isArray(entry)) {
              pushKey(entry[0], entry[1]);
            } else if (typeof entry === "object") {
              if (entry.info_key) {
                pushKey(
                  entry.info_key,
                  entry.info_value ?? entry.info_value_string ?? ""
                );
              } else {
                Object.keys(entry).forEach((k) => pushKey(k, entry[k]));
              }
            }
          });
        } else if (rawInfos && typeof rawInfos === "object") {
          Object.values(rawInfos).forEach((val) => {
            if (Array.isArray(val)) {
              val.forEach((e, i) => {
                if (typeof e === "object") {
                  Object.keys(e).forEach((k) => pushKey(k, e[k]));
                } else {
                  pushKey(infoKeys[i] ?? `info_${i + 1}`, "");
                }
              });
            } else if (typeof val === "object") {
              Object.keys(val).forEach((k) => pushKey(k, val[k]));
            }
          });
        }

        const additionalInfosPerStage = stageObj.additionalInfoKeys || {};
        const additionalKeysSet = new Set(
          Object.keys(additionalInfosPerStage).map((k) => String(k))
        );

        let stageMeta = null;
        if (multistageMeta && Array.isArray(multistageMeta.stages)) {
          stageMeta =
            multistageMeta.stages.find(
              (s) => String(s.name) === String(stageObj.stage)
            ) ||
            multistageMeta.stages[idx] ||
            null;
        }

        const sourceChoices =
          (stageMeta &&
            Array.isArray(stageMeta.choices) &&
            stageMeta.choices) ||
          (Array.isArray(stageObj.choices) && stageObj.choices) ||
          [];

        const isHeaderLike = (v) => {
          if (v == null) return false;
          if (
            Array.isArray(v) &&
            v.length > 0 &&
            v.every((x) => typeof x === "string")
          )
            return true;
          return false;
        };

        const getInfosFromChoice = (choice) => {
          if (!choice) return null;
          const infos =
            choice.infos ?? choice.info_columns ?? choice.infos_columns ?? [];
          if (!Array.isArray(infos)) return null;
          const obj = {};
          infos.forEach((entry) => {
            if (!entry) return;
            if (typeof entry === "object" && !Array.isArray(entry)) {
              const keys = Object.keys(entry);
              if (keys.length === 2 && (entry.info_key || entry.info_value)) {
                const k = entry.info_key ?? keys[0];
                const v =
                  entry.info_value ??
                  entry[entry.info_key] ??
                  entry[keys[1]] ??
                  "";
                if (k) obj[String(k)] = v;
              } else {
                keys.forEach((k) => {
                  obj[String(k)] = entry[k];
                });
              }
            } else if (Array.isArray(entry) && entry.length >= 2) {
              obj[String(entry[0])] = entry[1];
            }
          });
          return obj;
        };

        const choiceIdToPos = {};
        sourceChoices.forEach((c, i) => {
          const cid = String(
            c.id ?? c.choice_id ?? c.choiceId ?? c.key ?? c.value ?? ""
          );
          if (cid) choiceIdToPos[cid] = String(i);
          if (c.value !== undefined) choiceIdToPos[String(c.value)] = String(i);
          if (c.name !== undefined) choiceIdToPos[String(c.name)] = String(i);
        });

        const findAdditionalKey = (rawKey) => {
          if (rawKey === undefined || rawKey === null) return null;
          const s = String(rawKey);
          if (additionalKeysSet.has(s)) return s;
          if (additionalKeysSet.has(String(Number(s))))
            return String(Number(s));
          if (
            choiceIdToPos[String(s)] &&
            additionalKeysSet.has(choiceIdToPos[String(s)])
          )
            return choiceIdToPos[String(s)];
          const n = Number(s);
          if (!Number.isNaN(n)) {
            for (const k of additionalKeysSet) {
              if (String(n) === String(k)) return k;
            }
          }

          for (const [choiceId, pos] of Object.entries(choiceIdToPos)) {
            if (
              String(choiceId) === String(rawKey) &&
              additionalKeysSet.has(String(pos))
            )
              return String(pos);
          }
          return null;
        };

        const resolveAdditionalForChoice = (map, choiceKey) => {
          if (!map) return null;
          const tryKeys = [choiceKey, String(choiceKey), Number(choiceKey)];
          for (const k of tryKeys) {
            if (k === undefined || k === null) continue;
            if (Object.prototype.hasOwnProperty.call(map, k)) return map[k];
          }
          if (Array.isArray(map)) {
            for (const el of map) {
              if (!el) continue;
              if (Array.isArray(el) && el.length > 0) {
                if (String(el[0]) === String(choiceKey))
                  return el[1] ?? el[2] ?? null;
              } else if (typeof el === "object") {
                if (
                  el.choice_id !== undefined &&
                  String(el.choice_id) === String(choiceKey)
                )
                  return el.infos ?? el.additional ?? el;
                if (
                  el.choiceId !== undefined &&
                  String(el.choiceId) === String(choiceKey)
                )
                  return el.infos ?? el.additional ?? el;
                if (Object.prototype.hasOwnProperty.call(el, String(choiceKey)))
                  return el[String(choiceKey)];
              }
            }
          }
          return null;
        };

        const normalizeChoiceAdditional = (raw) => {
          if (raw == null) return {};
          if (typeof raw === "object" && !Array.isArray(raw)) {
            const keys = Object.keys(raw);
            const isIndexLike =
              keys.length > 0 && keys.every((k) => String(parseInt(k)) === k);
            if (isIndexLike && infoKeys.length > 0) {
              const arr = keys.map((k) => raw[k]);
              const obj = {};
              arr.forEach((v, i) => {
                const ik = infoKeys[i] ?? `info_${i + 1}`;
                obj[ik] = v;
              });
              return obj;
            }
            return { ...raw };
          }
          if (Array.isArray(raw)) {
            const allSingleKeyObjects = raw.every(
              (a) =>
                a &&
                typeof a === "object" &&
                !Array.isArray(a) &&
                Object.keys(a).length === 1
            );
            if (allSingleKeyObjects) {
              const obj = {};
              raw.forEach((a) => {
                const k = Object.keys(a)[0];
                obj[k] = a[k];
              });
              return obj;
            }
            if (infoKeys.length > 0) {
              const obj = {};
              raw.forEach((v, i) => {
                const ik = infoKeys[i] ?? `info_${i + 1}`;
                obj[ik] = v;
              });
              return obj;
            }
            const merged = {};
            raw.forEach((it) => {
              if (it && typeof it === "object" && !Array.isArray(it))
                Object.assign(merged, it);
            });
            return merged;
          }
          if (infoKeys.length > 0) return { [infoKeys[0]]: raw };
          return { info: raw };
        };

        const groupData = [];
        for (const res of resultsArr) {
          try {
            const name = res?.[0]?.[1] ?? "";
            const email = res?.[1] ?? "";
            const rawGroupName = res?.[2]?.[1];
            const groupName =
              rawGroupName === "Absent"
                ? t("Ei paikalla")
                : (rawGroupName ?? "");
            let choiceIndex = res?.[3] ?? res?.[2]?.[2] ?? "";
            if (choiceIndex === null || choiceIndex === undefined)
              choiceIndex = "";

            const choiceKey = res?.[2]?.[0] ?? choiceIndex;
            const canonical = findAdditionalKey(choiceKey);
            let rawForChoice = canonical
              ? additionalInfosPerStage[canonical]
              : resolveAdditionalForChoice(additionalInfosPerStage, choiceKey);

            if (isHeaderLike(rawForChoice)) rawForChoice = null;

            if (!rawForChoice) {
              const matchedChoice =
                sourceChoices.find(
                  (c) =>
                    String(c.id) === String(choiceKey) ||
                    String(c.choice_id) === String(choiceKey) ||
                    String(c.choiceId) === String(choiceKey) ||
                    String(c.name) === String(choiceKey)
                ) ?? null;
              if (matchedChoice) {
                rawForChoice = getInfosFromChoice(matchedChoice);
              }
            }

            if (!rawForChoice)
              rawForChoice = resolveAdditionalForChoice(
                additionalInfosPerStage,
                choiceKey
              );

            const normalized = normalizeChoiceAdditional(rawForChoice);

            const additional = {};
            infoKeys.forEach((ik) => {
              let v = normalized?.[ik];
              if (v === undefined || v === null || v === "") {
                v = infoDefaults[ik] ?? "";
              }
              additional[ik] = v;
            });

            groupData.push({
              [t("Nimi")]: name,
              [t("Sähköposti")]: email,
              [t("Ryhmä")]: groupName,
              [t("Monesko valinta")]: choiceIndex,
              ...additional
            });
          } catch (rowErr) {
            groupData.push({
              [t("Virheellinen rivi")]: t("Tieto puuttuu tai on rikkoutunut")
            });
          }
        }

        if (groupData.length === 0) {
          groupData.push({
            [t("Info")]: t("Kaikki rivit olivat virheellisiä")
          });
        }

        const ws = XLSX.utils.json_to_sheet(groupData);
        XLSX.utils.book_append_sheet(wb, ws, sheetName);
      } catch (stageErr) {
        const errRow = { [t("Virhe")]: t("Tämän vaiheen vienti epäonnistui") };
        const rawName = stageObj?.stage || `${t("vaihe")}_${idx + 1}`;
        const sheetName = String(rawName).substring(0, 31);
        const ws = XLSX.utils.json_to_sheet([errRow]);
        XLSX.utils.book_append_sheet(wb, ws, sheetName);
      }
    }

    try {
      const filename = `${t("tulokset")}_${id || "multivaiheinen"}.xlsx`;
      XLSX.writeFile(wb, filename);
    } catch (writeErr) {
      showNotification(t("Tulosten vienti epäonnistui"), "error");
      console.error("Excel write error", writeErr);
    }
  };

  const saveAllResults = () => {
    try {
      surveyService.saveMultistageResults(id);
      showNotification(t("Kaikkien vaiheiden tulokset tallennettu"), "success");
      setResultsSaved(true);
    } catch (err) {
      showNotification(t("Tulosten tallennus epäonnistui"), "error");
      console.error("Error saving all results", err);
    }
  };

  if (loading)
    return <div className="text-center mt-5">{t("Ladataan...")}</div>;

  return (
    <div>
      <h2>{t("Monivaiheisen kyselyn tulokset")}</h2>

      <div style={{ marginTop: "0.5em", marginBottom: "0.5em" }}>
        <button
          className="btn btn-outline-primary"
          style={{ marginTop: "1em", marginBottom: "1em" }}
          onClick={exportToExcel}
        >
          {t("Vie tulokset Excel-taulukkoon")}
        </button>
        &nbsp;
        <div>
          {!resultsSaved && (
            <button
              className="btn btn-outline-success"
              onClick={saveAllResults}
            >
              {t("Tallenna kaikkien vaiheiden tulokset")}
            </button>
          )}
        </div>
      </div>

      <div style={{ marginBottom: "1em" }}>
        <StageDropdown
          stages={stages}
          currStage={currStage}
          setCurrStage={setCurrStage}
        />
      </div>

      {currResults && (
        <>
          <Happiness
            average={currResults.happiness}
            happinessData={happinessData}
          />
          {droppedGroups && droppedGroups.length > 0 && (
            <div style={{ marginTop: "1em", marginBottom: "2em" }}>
              <b style={{ color: "orangered" }}>
                {t("Ryhmät, jotka pudotettiin jaosta")}
              </b>
              <ul>
                {droppedGroups.map((group, i) => (
                  <li key={i} style={{ color: "orangered" }}>
                    {group}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <p>
            <b>{t("Opiskelijat on lajiteltu ryhmiin seuraavasti")}:</b>
          </p>

          <SurveyResultsTable
            results={results}
            surveyId={id}
            currStage={currStage}
          />
        </>
      )}

      {!currResults && <p>{t("Ei tuloksia tälle vaiheelle")}</p>}
    </div>
  );
};

export default MultistageSurveyResultsPage;
