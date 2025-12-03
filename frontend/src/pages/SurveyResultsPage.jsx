import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useNotification } from "../context/NotificationContext";
import surveyService from "../services/surveys";
import SurveyResultsTable from "../components/survey_results_page_components/SurveyResultsTable";
import Happiness from "../components/survey_results_page_components/Happiness";

const SurveyResultsPage = () => {
  const [surveyResultsData, setSurveyResultsData] = useState({});
  const [droppedGroups, setDroppedGroups] = useState([]);
  const [infoKeys, setInfoKeys] = useState([]);
  const [additionalInfos, setAdditionalInfos] = useState([]);
  const [happinessData, setHappinessData] = useState([]);
  const [results, setResults] = useState([]);
  const [resultsSaved, setResultsSaved] = useState(false);
  const [loading, setLoading] = useState(true);

  const { t } = useTranslation();
  const { id } = useParams();
  const { showNotification } = useNotification();
  const navigate = useNavigate();

  useEffect(() => {
    const getSurveyResults = async () => {
      try {
        const isMultistage = await surveyService.isMultistage(id);
        if (isMultistage) {
          navigate(`/surveys/multistage/${id}/results`, { replace: true });
        }
        const response = await surveyService.getSurveyResultsData(id);
        if (!response.results) {
          navigate(`/surveys/${id}/answers`, { replace: true });
        }
        setSurveyResultsData(response);
        setDroppedGroups(response.droppedGroups);
        setResults(response.results);
        setHappinessData(response.happinessData);
        setInfoKeys(response.infos);
        setAdditionalInfos(response.additionalInfoKeys);
        setResultsSaved(response.resultsSaved);
      } catch (err) {
        console.error("error loading survey results", err);
      } finally {
        setTimeout(() => {
          setLoading(false);
        }, 1);
      }
    };
    getSurveyResults();
  }, []);

  const handleToExcelFile = async () => {
    try {
      if (!results || results.length === 0) {
        showNotification(t("Ei tuloksia vietäväksi"), "warning");
        return;
      }

      let surveyMeta = null;
      try {
        surveyMeta = await surveyService.getSurvey(id);
      } catch (err) {
        console.warn("Could not load survey metadata for infos lookup", err);
      }

      const rawInfos = infoKeys ?? [];
      const infoKeyNames = [];
      const infoDefaults = {};
      const pushKey = (k, def) => {
        if (!k && k !== 0) return;
        const sk = String(k);
        if (!infoKeyNames.includes(sk)) infoKeyNames.push(sk);
        if (def !== undefined && def !== null && infoDefaults[sk] === undefined)
          infoDefaults[sk] = def;
      };

      if (Array.isArray(rawInfos)) {
        rawInfos.forEach((entry) => {
          if (!entry) return;
          if (typeof entry === "string") pushKey(entry, "");
          else if (Array.isArray(entry)) pushKey(entry[0], entry[1]);
          else if (typeof entry === "object") {
            if (entry.info_key)
              pushKey(
                entry.info_key,
                entry.info_value ?? entry.info_value_string ?? ""
              );
            else Object.keys(entry).forEach((k) => pushKey(k, entry[k]));
          }
        });
      }

      const additionalInfosPerSurvey = additionalInfos || {};
      const additionalKeysSet = new Set(
        Object.keys(additionalInfosPerSurvey).map((k) => String(k))
      );

      const sourceChoices =
        (surveyMeta &&
          Array.isArray(surveyMeta.choices) &&
          surveyMeta.choices) ||
        (surveyResultsData &&
          Array.isArray(surveyResultsData.choices) &&
          surveyResultsData.choices) ||
        [];
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
        if (additionalKeysSet.has(String(Number(s)))) return String(Number(s));
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
          if (isIndexLike && infoKeyNames.length > 0) {
            const arr = keys.map((k) => raw[k]);
            const obj = {};
            arr.forEach((v, i) => {
              const ik = infoKeyNames[i] ?? `info_${i + 1}`;
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
          if (infoKeyNames.length > 0) {
            const obj = {};
            raw.forEach((v, i) => {
              const ik = infoKeyNames[i] ?? `info_${i + 1}`;
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
        if (infoKeyNames.length > 0) return { [infoKeyNames[0]]: raw };
        return { info: raw };
      };

      const groupData = [];

      results.forEach((res) => {
        try {
          const name = res?.[0]?.[1] ?? "";
          const email = res?.[1] ?? "";
          const groupName = res?.[2]?.[1] ?? "";
          let choiceIndex = res?.[3] ?? res?.[2]?.[2] ?? "";
          if (choiceIndex === null || choiceIndex === undefined)
            choiceIndex = "";

          const choiceKey = res?.[2]?.[0] ?? choiceIndex;
          const canonical = findAdditionalKey(choiceKey);
          let rawForChoice = canonical
            ? additionalInfosPerSurvey[canonical]
            : resolveAdditionalForChoice(additionalInfosPerSurvey, choiceKey);

          const isHeaderLike = (v) =>
            Array.isArray(v) &&
            v.length > 0 &&
            v.every((x) => typeof x === "string");
          if (isHeaderLike(rawForChoice)) rawForChoice = null;

          if (!rawForChoice && sourceChoices.length > 0) {
            const matchedChoice =
              sourceChoices.find(
                (c) =>
                  String(c.id) === String(choiceKey) ||
                  String(c.choice_id) === String(choiceKey) ||
                  String(c.choiceId) === String(choiceKey) ||
                  String(c.name) === String(choiceKey)
              ) ?? null;

            if (matchedChoice) {
              const infos =
                matchedChoice.infos ?? matchedChoice.info_columns ?? [];
              if (Array.isArray(infos) && infos.length > 0) {
                const obj = {};
                infos.forEach((entry) => {
                  if (!entry) return;
                  if (typeof entry === "object" && !Array.isArray(entry)) {
                    const keys = Object.keys(entry);
                    if (
                      keys.length === 2 &&
                      (entry.info_key || entry.info_value)
                    ) {
                      const k = entry.info_key ?? keys[0];
                      const v =
                        entry.info_value ??
                        entry[entry.info_key] ??
                        entry[keys[1]] ??
                        "";
                      if (k) obj[String(k)] = v;
                    } else {
                      keys.forEach((k) => (obj[String(k)] = entry[k]));
                    }
                  } else if (Array.isArray(entry) && entry.length >= 2) {
                    obj[String(entry[0])] = entry[1];
                  }
                });
                rawForChoice = obj;
              }
            }
          }

          if (!rawForChoice)
            rawForChoice = resolveAdditionalForChoice(
              additionalInfosPerSurvey,
              choiceKey
            );

          const normalized = normalizeChoiceAdditional(rawForChoice);

          const additional = {};
          infoKeyNames.forEach((ik) => {
            let v = normalized?.[ik];
            if (v === undefined || v === null || v === "")
              v = infoDefaults[ik] ?? "";
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
      });

      if (groupData.length === 0) {
        groupData.push({ [t("Info")]: t("Kaikki rivit olivat virheellisiä") });
      }

      const { utils, writeFile } = await import("xlsx");
      const { json_to_sheet, book_new, book_append_sheet } = utils;
      const ws = json_to_sheet(groupData);
      const wb = book_new();
      book_append_sheet(wb, ws, t("Tulokset"));
      writeFile(wb, `${t("tulokset")}.xlsx`);
    } catch (err) {
      showNotification(t("Tulosten vienti epäonnistui"), "error");
      console.error("Excel write error", err);
    }
  };

  const handleSaveResults = () => {
    try {
      surveyService.saveResults(id);
      showNotification(t("Ryhmäjako tallennettu"), "success");
      setResultsSaved(true);
    } catch (err) {
      showNotification(t("Ryhmäjaon tallennus epäonnistui"), "error");
      console.error("Error saving results", err);
    }
  };

  if (loading)
    return <div className="text-center mt-5">{t("Ladataan...")}</div>;

  return (
    <div>
      <h2>{t("Lajittelun tulokset")}</h2>
      <Happiness
        average={surveyResultsData.happiness}
        happinessData={happinessData}
      />
      <div>
        <button
          className="btn btn-outline-primary"
          onClick={handleToExcelFile}
          style={{ marginTop: "1em", marginBottom: "1em" }}
        >
          {t("Vie tulokset Excel-taulukkoon")}
        </button>
      </div>
      <div>
        {!resultsSaved && (
          <button
            className="btn btn-outline-success"
            onClick={handleSaveResults}
            style={{ marginBottom: "2em" }}
          >
            {t("Tallenna tulokset")}
          </button>
        )}
      </div>
      {droppedGroups.length > 0 && (
        <div>
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
      <SurveyResultsTable results={results} surveyId={id} />
    </div>
  );
};

export default SurveyResultsPage;
