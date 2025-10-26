import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import * as XLSX from "xlsx";
import surveyService from "../services/surveys";
import SurveyResultsTable from "../components/survey_results_page_components/SurveyResultsTable";

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
  const navigate = useNavigate();

  useEffect(() => {
    const getSurveyResults = async () => {
      try {
        const response = await surveyService.getSurveyResultsData(id);
        if (!response.results) {
          // notification here
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

  const handleToExcelFile = () => {
    const groupData = results.map((res) => ({
      [t("Nimi")]: res[0][1],
      [t("Sähköposti")]: res[1],
      [t("Ryhmä")]: res[2][1],
      [t("Monesko valinta")]: res[3],
      ...Object.fromEntries(
        infoKeys.map((pair, index) => [
          pair.info_key,
          additionalInfos[res[2][0]][index]
        ])
      )
    }));
    const ws = XLSX.utils.json_to_sheet(groupData);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, t("Tulokset"));
    XLSX.writeFile(wb, `${t("tulokset")}.xlsx`);
  };

  const handleSaveResults = () => {
    try {
      surveyService.saveResults(id);
      // success notification here
      setResultsSaved(true);
    } catch (err) {
      // error notification here
      console.error("Error saving results", err);
    }
  };

  if (loading) return null;

  return (
    <div>
      <h2>{t("Lajittelun tulokset")}</h2>
      <b>
        {t("Ryhmävalintojen keskiarvo")}: {surveyResultsData.happiness}
      </b>
      <div>
        {/* translations will fail here */}
        {happinessData.map((h, i) => (
          <div key={i}>
            <label>
              {h[0]}
              {h[1]}
            </label>
          </div>
        ))}
      </div>
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
