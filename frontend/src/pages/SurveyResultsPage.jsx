import { useTranslation } from "react-i18next";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import surveyService from "../services/surveys";
import SurveyResultsTable from "../components/survey_results_page_components/SurveyResultsTable";

const SurveyResultsPage = () => {
  const [surveyResultsData, setSurveyResultsData] = useState({});
  const [droppedGroups, setDroppedGroups] = useState([]);
  const [happinessData, setHappinessData] = useState([]);
  const [results, setResults] = useState([]);

  const { t } = useTranslation();
  const { id } = useParams();

  useEffect(() => {
    const getSurveyResults = async () => {
      try {
        const response = await surveyService.getSurveyResultsData(id);
        setSurveyResultsData(response);
        setDroppedGroups(response.droppedGroups);
        setResults(response.results);
        setHappinessData(response.happinessData);
        console.log(response)
      } catch (err) {
        console.error("error loading survey results", err)
      }
    } 
    getSurveyResults();
  }, [])

  return (
    <div>
      <h2>{t("Lajittelun tulokset")}</h2>
      <b>{t("Ryhmävalintojen keskiarvo")}: {surveyResultsData.happiness}</b>
      <div>
        {/* translations will fail here */}
        {happinessData.map((h, i) =>
          <div>
            <label key={i}>
              {h[0]}{h[1]}
            </label>
          </div>
        )}
      </div>
      <div>
        <button 
          className="btn btn-outline-primary"
          style={{marginTop: "1em"}}
          >
            {t("Vie tulokset Excel-taulukkoon")}
        </button>
      </div>
      <div>
        <button 
          className="btn btn-outline-success"
          style={{marginTop: "1em", marginBottom: "2em"}}
          >
            {t("Tallenna tulokset")}
        </button>
      </div>
      {droppedGroups.length > 0 && (
        <div>
          <b style={{ color: "orangered" }}>{t("Ryhmät, jotka pudotettiin jaosta")}</b>
          <ul>
            {droppedGroups.map((group, i) => 
              <li key={i} style={{ color: "orangered" }}>
                {group}
              </li>)}
          </ul>
        </div>
      )}
      <p>
        <b>{t("Opiskelijat on lajiteltu ryhmiin seuraavasti")}:</b>
      </p>
      <SurveyResultsTable results={results} />
    </div>
  )    
}

export default SurveyResultsPage;