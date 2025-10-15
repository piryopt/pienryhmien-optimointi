import { useState, useEffect } from "react";
import surveyService from "../serivces/surveys";

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
        <h1>Aiemmat kyselyt</h1>
        {activeSurveys.map(a => <p>{a.surveyname}</p>)}
        ----------------------
        {closedSurveys.map(c => <p>{c.surveyname}</p>)}
      </div>
  );
};

export default SurveysPage;