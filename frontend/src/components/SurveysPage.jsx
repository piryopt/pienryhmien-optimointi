import { useState, useEffect } from "react";
import surveyService from "../serivces/surveys";
import SurveysTable from "./surveys_page_components/SurveysTable";

const SurveysPage = () => {
  const [activeSurveys, setActiveSurveys] = useState([]);
  const [closedSurveys, setClosedSurveys] = useState([]);
  
  useEffect(() => {
    Promise.all([
      surveyService.getActiveSurveys(),
      surveyService.getClosedSurveys()
    ])
    .then(([activeRes, closedRes]) => {
        setActiveSurveys(activeRes.data);
        setClosedSurveys(closedRes.data);
    })
    .catch(err => {
      console.error("Error loading surveys", err);
    });
  }, []);
  
  return (
    <div>
      <h2>Aiemmat</h2>
      <SurveysTable activeSurveys={activeSurveys} closedSurveys={closedSurveys} />
    </div>
  );
};

export default SurveysPage;