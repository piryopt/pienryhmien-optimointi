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
    if (!results || results.length === 0) {
      showNotification(t("Ei tuloksia vietäväksi"), "warning")
      return
    }
    
    // info key sanitization
    const safeInfoKeys = Array.isArray(infoKeys) ? infoKeys.filter(k => k && k.info_key) : []

    const groupData = results.map((res) => {
      const name = res?.[0]?.[1] ?? ""
      const email = res?.[1] ?? ""
      const groupName = res?.[2]?.[1] ?? ""
      // fallback for choice ordinal
      const choiceIndex = (res?.[3] ?? res?.[2]?.[2] ?? "") || ""

      const additional = Object.fromEntries(
        safeInfoKeys
          .map((pair, index) => [pair.info_key, (additionalInfos?.[res?.[2]?.[0]] || [])[index]])
          .filter(([key, value]) => key && value !== undefined && value !== null && value !== "")
      )

      return {
        [t("Nimi")]: name,
        [t("Sähköposti")]: email,
        [t("Ryhmä")]: groupName,
        [t("Monesko valinta")]: choiceIndex,
        ...additional
      }
    })
    const { utils, writeFile } = await import("xlsx");
    const { json_to_sheet, book_new, book_append_sheet } = utils;
    const ws = json_to_sheet(groupData);
    const wb = book_new();
    book_append_sheet(wb, ws, t("Tulokset"));
    writeFile(wb, `${t("tulokset")}.xlsx`);
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

  if (loading) return null;

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
