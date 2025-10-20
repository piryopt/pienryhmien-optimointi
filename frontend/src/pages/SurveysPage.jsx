import { useState, useEffect } from "react";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import SurveysTable from "../components/surveys_page_components/SurveysTable";
import listWhite from "/images/list_white_36dp.svg";

const SurveysPage = () => {
  const [activeSurveys, setActiveSurveys] = useState([]);
  const [closedSurveys, setClosedSurveys] = useState([]);
  const { t } = useTranslation();

  useEffect(() => {
    const getSurveys = async () => {
        try {
        const [activeRes, closedRes] = await Promise.all([
        surveyService.getActiveSurveys(),
        surveyService.getClosedSurveys()
      ])
      setActiveSurveys(activeRes);
      setClosedSurveys(closedRes);
      } catch (err) {
        console.error("Error loading surveys", err)
      }
    }
    getSurveys()
  }, []);
  
  return (
    <div>
      <br />
      <h2>
        <img
          src={listWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="42"
          height="47"
        />
        &nbsp;{t("Aiemmat kyselyt")}
      </h2>
      <br />
      <SurveysTable 
        activeSurveys={activeSurveys} 
        closedSurveys={closedSurveys}
        setActiveSurveys={setActiveSurveys}
        setClosedSurveys={setClosedSurveys}
      />
    </div>
  );
};

export default SurveysPage;