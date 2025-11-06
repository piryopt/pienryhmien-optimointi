import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { useTranslation } from "react-i18next";
import surveyService from "../services/surveys";
import assignmentWhite from "/images/assignment_white_36dp.svg";
import SurveyAnswersTable from "../components/survey_answers_page_components/SurveyAnswersTable";
import StageDropdown from "../components/survey_answers_page_components/StageDropdown";

const SurveyMultistageAnswersPage = () => {
  const { surveyId } = useParams();
  const { t } = useTranslation();
  const [surveyData, setSurveyData] = useState({});
  const [surveyAnswers, setSurveyAnswers] = useState({});
  const [stages, setStages] = useState([]);
  const [currStage, setCurrStage] = useState(null);

  useEffect(() => {
    const getSurveyAnswers = async () => {
      const response =
        await surveyService.getMultiStageSurveyAnswersData(surveyId);
      setSurveyData(response);
      setSurveyAnswers(response.answers);
      const surveyStages = Object.keys(response.answers);
      setStages(surveyStages);
      setCurrStage(surveyStages[0]);
    };
    getSurveyAnswers();
  }, []);
  return (
    <div>
      <h5>
        <img src={assignmentWhite} alt="" width={34} height={30} />
        &nbsp;{surveyData.surveyName}
      </h5>
      <StageDropdown
        stages={stages}
        currStage={currStage}
        setCurrStage={setCurrStage}
      />
      {currStage && (
        <SurveyAnswersTable
          answers={surveyAnswers[currStage]}
          setAnswers={null}
          filteredAnswers={surveyAnswers[currStage]}
          setFilteredAnswers={null}
          surveyId={null}
          setSurveyAnswersAmount={null}
        />
      )}
    </div>
  );
};

export default SurveyMultistageAnswersPage;
