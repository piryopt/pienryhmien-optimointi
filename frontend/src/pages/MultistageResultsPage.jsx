import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import surveyService from "../services/surveys";
import StageDropdown from "../components/survey_answers_page_components/StageDropdown";

const MultistageSurveyResultsPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [surveyResultsData, setSurveyResultsData] = useState(null);
  const [stages, setStages] = useState([]);
  const [currStage, setCurrStage] = useState(null);
  const [currResults, setCurrResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getSurveyResults = async () => {
      try {
        const response = await surveyService.getSurveyResultsData(id);
        if (!response.stageResults) {
        navigate(`/surveys/multistage/${id}/answers`, { replace: true });
      }
        setSurveyResultsData(response);
        const surveyStages = response.stageResults.map((stage) => stage["stage"]);
        setStages(surveyStages);
        setCurrStage(surveyStages[0]);
        setCurrResults(response.stageResults[0]);
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

  useEffect(() => {
    if (!surveyResultsData || !Array.isArray(surveyResultsData.stageResults)) return;
    const active = surveyResultsData.stageResults.find((s) => s.stage === currStage)
      || surveyResultsData.stageResults[0]
      || null;
    setCurrResults(active);
  }, [currStage, surveyResultsData]);

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <StageDropdown
        stages={stages}
        currStage={currStage}
        setCurrStage={setCurrStage}
      />
      <p style={{color:"white"}}>{JSON.stringify(currResults, null, 2)}</p>
    </div>
  );
}

export default MultistageSurveyResultsPage;