import { useState, useEffect } from "react";
import surveyService from "../serivces/surveys";
import SurveysTable from "./surveys_page_components/SurveysTable";
import listWhite from "../static/images/list_white_36dp.svg";

const SurveysPage = () => {
  const [activeSurveys, setActiveSurveys] = useState([]);
  const [closedSurveys, setClosedSurveys] = useState([]);
  
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
      <h2>
        <img
          src={listWhite}
          alt=""
          className="d-inline-block align-text-top"
          width="42"
          height="47"
        />
        &nbsp;Aiemmat kyselyt
      </h2>
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